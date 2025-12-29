# MDpad 📝  
*A Notepad-like desktop editor for Markdown with live preview*

MDpad is a lightweight, fast, and beautiful Markdown editor built with **Python + Tkinter**.  
It provides a **plain-text editing experience** on the left and a **live HTML preview** on the right using an embedded Chromium browser.

Perfect for quick notes, documentation, and README writing — without the bloat of full IDEs.

---

## ✨ Features

- 📝 **Minimal Markdown editor** (Notepad-style)
- 👀 **Live preview** rendered instantly as you type
- 🌑 **Dark theme** (editor + preview)
- 📄 Supports tables, fenced code blocks, blockquotes, and more
- 🌐 Chromium-based embedded preview (`tkinterweb`)
- 💾 Open, Save, Save As support
- 🧠 Undo / Redo
- 🚀 Launch files via *“Open with”* from File Explorer

---

## 📸 Preview

> Left: Markdown editor  
> Right: Live rendered preview

*(Screenshot coming soon)*

---

## 🛠️ Requirements

- **Python 3.10+**
- pip packages:
  - `markdown`
  - `tkinterweb`

> Tkinter comes pre-installed with most Python distributions.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/mdpad.git
cd mdpad

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

```

