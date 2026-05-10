import sys
import os
import asyncio
import threading
from playwright.async_api import async_playwright
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Konfiguration
MAX_CACHE_SIZE_MB = 100  # Höheres Limit für Videos
captured_data = {}      

class NetFishApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NET-fish 🎣 - Network Stream Sniffer")
        self.geometry("1100x700")

        # UI Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="NET-fish 🎣", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        # Filter-Bereich
        self.filter_label = ctk.CTkLabel(self.sidebar, text="Filter (z.B. mp4, jpg, pdf):")
        self.filter_label.pack(padx=10, pady=(10, 0))
        
        self.filter_entry = ctk.CTkEntry(self.sidebar, placeholder_text="mp4, png, ts, pdf")
        self.filter_entry.insert(0, "mp4, png, jpg, pdf, ts") # Standard-Filter
        self.filter_entry.pack(padx=10, pady=5, fill="x")

        self.start_btn = ctk.CTkButton(self.sidebar, text="Browser Starten", command=self.start_sniffing_thread, fg_color="green", hover_color="darkgreen")
        self.start_btn.pack(pady=20, padx=10)

        self.save_btn = ctk.CTkButton(self.sidebar, text="Datei speichern (ID)", command=self.save_selected_file, state="disabled")
        self.save_btn.pack(pady=10, padx=10)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Bereit", text_color="yellow")
        self.status_label.pack(pady=10)

        self.info_label = ctk.CTkLabel(self.sidebar, text="Cache: 0 Dateien", font=("Arial", 11))
        self.info_label.pack(side="bottom", pady=20)

        # --- Main Content ---
        self.file_list = ctk.CTkTextbox(self, width=600, font=("Courier New", 12))
        self.file_list.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.log("NET-fish bereit. Bitte Filter setzen und Browser starten.")
        
        self.detected_urls = []

    def log(self, message):
        self.file_list.insert("end", message + "\n")
        self.file_list.see("end")

    def get_active_filters(self):
        # Liest das Eingabefeld aus und macht eine Liste daraus
        filter_str = self.filter_entry.get().lower()
        filters = [f.strip() for f in filter_str.split(",") if f.strip()]
        return filters

    def start_sniffing_thread(self):
        self.status_label.configure(text="Status: Sniffing...", text_color="green")
        self.start_btn.configure(state="disabled")
        self.filter_entry.configure(state="disabled") # Filter sperren während Laufzeit
        threading.Thread(target=self.run_playwright, daemon=True).start()

    def run_playwright(self):
        asyncio.run(self.sniff_network())

    async def sniff_network(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            async def handle_response(response):
                try:
                    url = response.url.lower()
                    active_filters = self.get_active_filters()
                    
                    # Prüfen ob die URL eine der Endungen aus dem Filter enthält
                    if any(ext in url for ext in active_filters):
                        body = await response.body()
                        if not body: return

                        size_mb = len(body) / (1024 * 1024)

                        if size_mb <= MAX_CACHE_SIZE_MB:
                            file_id = str(len(self.detected_urls) + 1)
                            content_type = response.headers.get("content-type", "unknown")
                            
                            captured_data[file_id] = {
                                "url": url,
                                "content": body,
                                "ext": url.split(".")[-1].split("?")[0][:4] # Endung extrahieren
                            }
                            self.detected_urls.append(file_id)
                            
                            self.log(f"[{file_id}] {size_mb:.2f}MB | {content_type} | {url[:70]}...")
                            self.info_label.configure(text=f"Cache: {len(captured_data)} Dateien")
                            self.save_btn.configure(state="normal")
                except Exception:
                    pass 

            page.on("response", handle_response)
            
            while True:
                await asyncio.sleep(1)
                if not browser.is_connected():
                    break
            
            self.status_label.configure(text="Status: Beendet", text_color="red")
            self.start_btn.configure(state="normal")
            self.filter_entry.configure(state="normal")

    def save_selected_file(self):
        dialog = ctk.CTkInputDialog(text="Dateinummer [ID] eingeben:", title="Save File")
        file_id = dialog.get_input()

        if file_id in captured_data:
            file_info = captured_data[file_id]
            suggested_ext = file_info["ext"]
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{suggested_ext}",
                initialfile=f"caught_file_{file_id}.{suggested_ext}"
            )
            
            if file_path:
                with open(file_path, "wb") as f:
                    f.write(file_info["content"])
                messagebox.showinfo("NET-fish", "Datei erfolgreich aufgebaut!")
        else:
            messagebox.showerror("Fehler", "ID nicht im Cache gefunden.")

if __name__ == "__main__":
    app = NetFishApp()
    app.mainloop()