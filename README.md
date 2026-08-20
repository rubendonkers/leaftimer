# 🌿 LeafTimer • Windows 11 Shutdown Timer

> A simplistic, open source desktop shutdown timer for Windows 11.

![LeafTimer Banner](assets/app_icon.png)

---

## Features

- **Style**: Clean Windows 11 Fluent interface with soft organic cards, botanical sage and pine tones, and dark/light mode toggle (🌙 / ☀️).
- **Controls**:
  - Smooth interactive slider (1 to 180 minutes).
  - Quick-preset pills (`15m`, `30m`, `45m`, `60m`, `90m`, `2h`).
  - Fine-tuning stepper buttons (`-15m`, `-5m`, `+5m`, `+15m`).
- **Live Dynamic Countdown**: Digital clock display (`HH:MM:SS`) with real-time remaining countdown and target shutdown timestamp (e.g. *PC will turn off at 23:15:00*).
- **Multiple Actions**: Supports **Shutdown** (default), **Restart**, or **Sleep**.
- **Safe 1-Click Cancel**: The primary button transforms into `✕ Cancel Shutdown` while timing, immediately stopping the countdown and clearing all Windows OS shutdown schedules.
- **Zero Bloat & Zero Telemetry**: Operates 100% locally with no internet connection, no analytics, and no background services.

---

## Website Landing Page

A product landing page is included in **[`index.html`](index.html)**:
- **Interactive Live Demo Widget**: Users can test the timer UI and slider directly in their web browser.
- **Download Buttons**: Direct links for both the **Setup Installer** and **Portable Executable**.
- **Deploy Ready**: Can be deployed with 1 click to GitHub Pages, Netlify, or Vercel.

---

## How to Install & Run

You can choose how you'd like to use LeafTimer:

### Option 1: Standard Windows Setup Wizard (`LeafTimer-Setup.exe`)
1. Download or open **[`dist/LeafTimer-Setup.exe`](dist/LeafTimer-Setup.exe)**.
2. Follow the setup wizard to install LeafTimer into your programs folder.
3. Automatically adds shortcuts to your **Desktop** and **Windows Start Menu**.

### Option 2: Standalone Portable (`LeafTimer.exe`)
1. Download or open **[`dist/LeafTimer.exe`](dist/LeafTimer.exe)**.
2. Runs immediately with a double-click. No installation wizard required.
3. Perfect for USB drives or zero-install workflows.

### Option 3: Run with Python / Batch
If you prefer running directly from source code:
```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the app
python main.py
# Or double-click run.bat / main.pyw
```

---

## Project Structure

```text
shutdown-timer/
├── assets/                  # High-resolution botanical leaf icons (.png & .ico)
├── dist/                    # Compiled distribution binaries
│   ├── LeafTimer.exe        # Method 1: Portable standalone executable
│   └── LeafTimer-Setup.exe  # Method 2: Standard Windows setup installer wizard
├── tests/                   # Automated unit tests
│   └── test_timer.py
├── app.py                   # Main graphical user interface (CustomTkinter)
├── timer_engine.py          # Background timer loop & Windows OS command hooks
├── theme.py                 # Nature color palette & typography tokens
├── assets.py                # Procedural icon generator
├── setup_wizard.py          # Modern Setup Wizard installer GUI
├── build_exe.py             # PyInstaller build automation script
├── install.ps1 / .bat       # 1-click desktop & start menu shortcut installers
├── run.bat                  # 1-click batch launcher
├── index.html               # Product landing page & web preview
└── requirements.txt         # Python package dependencies
```

---

## Building from Source

To compile the binaries yourself:
```powershell
# Build the standalone portable executable:
python build_exe.py

# Build the setup installer:
python -m PyInstaller --noconsole --onefile --name LeafTimer-Setup --icon=assets\app_icon.ico --add-data="dist\LeafTimer.exe;dist" --add-data="assets;assets" setup_wizard.py
```

---

## License

This project is open source and available under the **MIT License**. You are free to use, modify, distribute, or sell it.
