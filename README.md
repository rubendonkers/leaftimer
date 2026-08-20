# LeafTimer

> A simplistic, open source desktop shutdown timer for Windows 11.


---

## Features

- **Simplistic & Modern**: Clean Windows 11 Fluent interface with soft organic cards, botanical sage and pine tones, and dark/light mode toggle (🌙 / ☀️).
- **Effortless Minute Controls**:
  - Smooth interactive slider (1 to 180 minutes).
  - Quick-preset pills (`15m`, `30m`, `45m`, `60m`, `90m`, `2h`).
  - Fine-tuning stepper buttons (`-15m`, `-5m`, `+5m`, `+15m`).
- **Live Dynamic Countdown**: Digital clock display (`HH:MM:SS`) with real-time remaining countdown and target shutdown timestamp (e.g. *PC will turn off at 23:15:00*).
- **Multiple Actions**: Supports **Shutdown** (default), **Restart**, or **Sleep**.
- **Safe 1-Click Cancel**: The primary button transforms into `✕ Cancel Shutdown` while timing, immediately stopping the countdown and clearing all Windows OS shutdown schedules.
- **Zero Bloat & Zero Telemetry**: Operates 100% locally with no internet connection, no analytics, and no background services.

---

## Website & Web Preview

A single-page landing page is included in **[`index.html`](index.html)**:
- **Interactive Live Demo**: Test the timer slider and presets directly in any browser.
- **Deploy Ready**: Host for free with 1 click on **GitHub Pages**, **Netlify**, or **Vercel**.

---

## Quick Start (Running from Source)

### 1. Prerequisites
- Python 3.10+ on Windows 10/11

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/rubendonkers/leaftimer.git
cd leaftimer

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Application
```powershell
python main.py
```

---

## Running Tests

Run the automated test suite with Python's built-in `unittest`:

```powershell
python -m unittest discover -s tests
```

---

## Building Standalone Executable (`.exe`)

To compile the standalone single-file Windows executable:

```powershell
python build_exe.py
```

The compiled binary will be output to `dist/LeafTimer.exe` (excluded from git tracking).

---

## Repository Structure

```text
leaftimer/
├── assets/                  # High-resolution application icons (.png & .ico)
├── tests/                   # Automated unit test suite
│   └── test_timer.py
├── app.py                   # Main Graphical User Interface (CustomTkinter)
├── timer_engine.py          # Background countdown loop & Windows shutdown hooks
├── theme.py                 # Botanical color palette & typography tokens
├── assets.py                # Procedural icon generator
├── build_exe.py             # PyInstaller build automation script
├── main.py                  # Application entry point
├── index.html               # Product landing page & interactive demo
├── requirements.txt         # Project dependencies
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
