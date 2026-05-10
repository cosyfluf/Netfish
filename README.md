# NET-fish 🎣
**Network Stream Sniffer & File Builder**

**NET-fish** is a powerful Python-based utility that allows you to "fish" data directly out of your browser's network stream. It intercepts binary data in real-time, caches it in your RAM, and allows you to reconstruct those streams into actual files on your hard drive.

## 🚀 Features

*   **Stream Fishing:** Intercepts data packets as they flow through the browser.
*   **Encrypted Traffic:** Works seamlessly with **HTTPS** by hooking into the browser's internal response handler.
*   **Live GUI:** A modern interface built with `CustomTkinter` to monitor the "catch" in real-time.
*   **Smart Caching:** Temporarily stores intercepted data in a local cache (RAM) for previewing before saving.
*   **Automatic Reconstruction:** Rebuilds fragmented network data back into original formats like `.pdf`, `.png`, `.mp4`, `.zip`, etc.

## 🛠 Installation

1. **Save the project files** to your local machine (ensure the main script is named `main.py`).
2. **Install the required Python libraries:**
   ```bash
   pip install playwright customtkinter
   ```
3. **Install the browser engine:**
   ```bash
   playwright install chromium
   ```

## 📖 How to Use

1. **Launch NET-fish:** Run the main script via terminal or CMD:
   ```bash
   python main.py
   ```
2. **Start the Browser:** Click the **"Browser Starten"** button in the GUI. This opens a Chromium instance connected to the sniffer.
3. **Browse:** Visit any website (e.g., a gallery, a document hoster, or a media site).
4. **Monitor the Stream:** The NET-fish GUI will list every "caught" file with an ID, its size, and its type.
5. **Reconstruct:** 
    *   Note the **[ID]** of the file you want from the log window.
    *   Click **"Markierte Datei speichern"**.
    *   Enter the ID when prompted and choose your save location.

---

## ⚖️ Disclaimer (Haftungsausschluss)

**English:**
**NET-fish** is provided for **educational and research purposes only**. The developer assumes no liability and is not responsible for any misuse or damage caused by this program. 
*   **Compliance:** You are solely responsible for complying with the Terms of Service (ToS) of any website you visit.
*   **Copyright:** Capturing and saving copyrighted material without permission may be illegal in your jurisdiction.
*   **Privacy:** Do not use this tool to intercept private data or violate the privacy of others.
*   **No Warranty:** This software is provided "as is" without warranty of any kind, express or implied.

**Deutsch:**
**NET-fish** wird ausschließlich zu **Bildungs- und Forschungszwecken** zur Verfügung gestellt. Der Entwickler übernimmt keine Haftung und ist nicht verantwortlich für Missbrauch oder Schäden, die durch dieses Programm entstehen.
*   **Einhaltung von Regeln:** Sie sind allein dafür verantwortlich, die Nutzungsbedingungen (ToS) der von Ihnen besuchten Webseiten einzuhalten.
*   **Urheberrecht:** Das Abfangen und Speichern von urheberrechtlich geschütztem Material ohne Erlaubnis kann in Ihrer Gerichtsbarkeit rechtswidrig sein.
*   **Datenschutz:** Verwenden Sie dieses Tool nicht, um private Daten abzufangen oder die Privatsphäre anderer zu verletzen.
*   **Keine Gewährleistung:** Die Software wird "wie besehen" (as is) ohne jegliche Gewährleistung oder Garantie bereitgestellt.

---

## 🛠 Requirements

*   **Python:** 3.8 or higher
*   **Core File:** `main.py`
*   **Libraries:** Playwright, CustomTkinter
*   **OS:** Windows, macOS, or Linux

## 📝 License

This project is licensed under the MIT License - feel free to use and modify it for personal use.

*Happy Fishing!* 🎣