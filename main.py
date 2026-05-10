import sys
import os
import asyncio
import threading
from playwright.async_api import async_playwright
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Konfiguration
MAX_CACHE_SIZE_MB = 10  # Dateien über 10MB werden nicht im RAM gecacht
captured_data = {}      # Speicher für: {url: {"content": bytes, "type": str}}

class Netfish(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Network Stream Sniffer & File Builder")
        self.geometry("900x600")

        # UI Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Linke Seite: Steuerung & Status
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Bereit", text_color="yellow")
        self.status_label.pack(pady=20, padx=10)

        self.start_btn = ctk.CTkButton(self.sidebar, text="Browser Starten", command=self.start_sniffing_thread)
        self.start_btn.pack(pady=10, padx=10)

        self.save_btn = ctk.CTkButton(self.sidebar, text="Markierte Datei speichern", command=self.save_selected_file, state="disabled")
        self.save_btn.pack(pady=10, padx=10)

        self.info_label = ctk.CTkLabel(self.sidebar, text="Cache: 0 Dateien", font=("Arial", 11))
        self.info_label.pack(side="bottom", pady=20)

        # Rechte Seite: Liste der abgefangenen Dateien
        self.file_list = ctk.CTkTextbox(self, width=600)
        self.file_list.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.file_list.insert("0.0", "Warte auf Datenstrom...\n" + "-"*50 + "\n")
        
        # Interne Liste für die Auswahl (einfaches Mapping)
        self.detected_urls = []

    def log(self, message):
        self.file_list.insert("end", message + "\n")
        self.file_list.see("end")

    def start_sniffing_thread(self):
        self.status_label.configure(text="Status: Sniffing...", text_color="green")
        self.start_btn.configure(state="disabled")
        # Starte Playwright in einem eigenen Thread, damit die GUI nicht einfriert
        threading.Thread(target=self.run_playwright, daemon=True).start()

    def run_playwright(self):
        asyncio.run(self.sniff_network())

    async def sniff_network(self):
        async with async_playwright() as p:
            # Startet Chrome. Du kannst auch einen bestehenden Browser nutzen,
            # aber das hier ist für die Entwicklung einfacher.
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # Event-Handler für Antworten
            async def handle_response(response):
                try:
                    url = response.url
                    content_type = response.headers.get("content-type", "")
                    
                    # Filtere uninteressante Dinge (wie kleine Tracker-Pixel)
                    if any(ext in url.lower() for ext in [".png", ".jpg", ".mp4", ".pdf", ".zip", ".json"]):
                        
                        # Body abrufen
                        body = await response.body()
                        size_mb = len(body) / (1024 * 1024)

                        if size_mb <= MAX_CACHE_SIZE_MB:
                            file_id = f"{len(self.detected_urls) + 1}"
                            captured_data[file_id] = {
                                "url": url,
                                "content": body,
                                "type": content_type
                            }
                            self.detected_urls.append(file_id)
                            
                            # UI Update
                            self.log(f"[{file_id}] {content_type} | {size_mb:.2f} MB | {url[:80]}...")
                            self.info_label.configure(text=f"Cache: {len(captured_data)} Dateien")
                            self.save_btn.configure(state="normal")
                except Exception:
                    pass # Fehler bei Streams oder geschlossenen Verbindungen ignorieren

            page.on("response", handle_response)
            
            self.log("Browser geöffnet. Navigiere zu einer Seite...")
            # Bleibe offen, bis der Browser manuell geschlossen wird
            while True:
                await asyncio.sleep(1)
                if browser.is_connected() == False:
                    break

    def save_selected_file(self):
        # Einfache Logik: Wir fragen nach der ID aus der Liste
        dialog = ctk.CTkInputDialog(text="Gib die [ID] der Datei ein, die du speichern willst:", title="Speichern")
        file_id = dialog.get_input()

        if file_id in captured_data:
            data = captured_data[file_id]
            # Dateiendung raten
            ext = data["url"].split(".")[-1].split("?")[0]
            if len(ext) > 4: ext = "bin"

            file_path = filedialog.asksaveasfilename(defaultextension=f".{ext}", initialfile=f"file_{file_id}.{ext}")
            
            if file_path:
                with open(file_path, "wb") as f:
                    f.write(data["content"])
                messagebox.showinfo("Erfolg", "Datei wurde erfolgreich aufgebaut und gespeichert!")
        else:
            messagebox.showerror("Fehler", "ID nicht gefunden.")

if __name__ == "__main__":
    app = Netfish()
    app.mainloop()
