# MDpad 📝  
*A Notepad-like desktop GUI editor for Markdown with live preview*

MDpad is a lightweight, fast, and beautiful **desktop GUI Markdown editor** built with **Python + Tkinter**.  
It offers a clean **plain-text editor** on the left and a **live rendered preview** on the right using an embedded Chromium browser.

Designed for simplicity — no clutter, no terminal usage required.

---

## ✨ Features

- 🖥️ **Native GUI application** (no console window)
- 📝 Minimal Markdown editor (Notepad-style)
- 👀 Live preview while typing
- 🌑 Dark theme (editor + preview)
- 📄 Supports tables, fenced code blocks, blockquotes, and more
- 🌐 Chromium-based embedded preview (`tkinterweb`)
- 💾 Open, Save, Save As
- 🧠 Undo / Redo
- 🚀 Supports *“Open with”* from File Explorer

---

## 📦 Precompiled Executables (Windows)

For users who **do not want to install Python**, MDpad is available as a **precompiled Windows executable**.

- Executables are located in the **`dist/` folder**
- Built as **GUI applications** (no terminal / console window)
- Ready to run — just double-click

### How to use
1. Go to the `dist/` directory
2. Run `MDpad.exe`
3. Start editing Markdown files immediately

> These executables were generated using tools like **PyInstaller** with GUI mode enabled.

---

## 🛠️ Requirements (Source Version Only)

If you prefer running from source:

- **Python 3.10+**
- pip packages:
  - `markdown`
  - `tkinterweb`

> Tkinter is included with standard Python installations.

---

## 📦 Installation (From Source)

Clone the repository:

```bash
git clone https://github.com/yourusername/mdpad.git
cd mdpad
```

Install dependencies:

```bash
pip install markdown tkinterweb
```

---

## ▶️ Usage

Run the app:

```bash
python mdpad.py
```

Open a Markdown file directly:

```bash
python mdpad.py README.md
```

Or right-click any `.md` file → **Open with → Python / MDpad**

---

## ⌨️ Keyboard Shortcuts

| Shortcut           | Action    |
| ------------------ | --------- |
| `Ctrl + O`         | Open file |
| `Ctrl + S`         | Save      |
| `Ctrl + Shift + S` | Save As   |
| `Ctrl + Z`         | Undo      |
| `Ctrl + Y`         | Redo      |

---

## 🧩 Supported Markdown Extensions

MDpad uses Python-Markdown with the following extensions enabled:

* Tables
* Fenced code blocks
* Code highlighting
* Table of contents
* Markdown inside HTML
* Newline → `<br>` support

---

## 🎨 Theming

* Editor theme: Tkinter dark mode
* Preview theme: Custom CSS
* Easy to customize by editing the `CSS` variable

---

## 📁 Project Structure

```
mdpad.py
README.md
```

Single-file application by design — simple and portable.

---

## 🚧 Planned Improvements

* Light / Dark theme toggle
* Syntax highlighting in editor
* File tabs
* Auto-save
* Export to HTML / PDF

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Author

Built with ❤️ by **Sunil Saragadam**

If you like this project, consider starring ⭐ it on GitHub!

