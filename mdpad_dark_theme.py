#!/usr/bin/env python3
"""
MDpad – a Notepad-like desktop app for Markdown
Beautiful live preview (Chromium inside Tkinter)
"""
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.scrolledtext as st
import tkinter.messagebox as mb
import sys, pathlib, tempfile, webbrowser, textwrap, os
import markdown

# ----------------------------------------------
# 1.  embedded browser pane (pip install tkinterweb)
# ----------------------------------------------
try:
    from tkinterweb import HtmlFrame          # Chromium-based <iframe> for Tk
except ImportError:
    mb.showerror("Missing package", "pip install tkinterweb")
    sys.exit(1)

# ----------------------------------------------
# 2.  CSS that makes the preview beautiful
# ----------------------------------------------
CSS = textwrap.dedent("""
<style>
body{
    font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    line-height:1.6;
    color:#e6e6e6;
    background:#0f1115;
    margin:40px auto;
    max-width:800px;
    padding:0 20px
}
h1,h2,h3,h4,h5,h6{color:#4ea1ff;margin-top:1.2em;margin-bottom:.6em}
code{
    background:#1e222a;
    padding:2px 4px;
    border-radius:4px;
    font-size:.9em;
    color:#ffcc66
}
pre{
    background:#0b0e14;
    color:#d4d4d4;
    padding:1em;
    overflow-x:auto;
    border-radius:6px;
    font-size:.88em
}
table{border-collapse:collapse;width:100%}
th,td{
    border:1px solid #333;
    padding:6px 10px
}
th{background:#1e222a}
blockquote{
    border-left:4px solid #4ea1ff;
    margin:1em 0;
    padding-left:1em;
    color:#aaa
}
a{color:#4ea1ff}
</style>
""")


# ----------------------------------------------
# 3.  main application
# ----------------------------------------------
class MdPad(tk.Tk):
    def __init__(self, filename=None):
        super().__init__()
        self.configure(bg="#1e222a")
        self.title("MDpad_Dark")
        self.geometry("1000x650")
        self.file: pathlib.Path | None = None
        self.preview_file = None
        self.build_ui()
        if filename:
            self.open_file(pathlib.Path(filename))

    # ---------- UI construction ----------
    def build_ui(self):
        # menu
        men = tk.Menu(self)
        self.config(menu=men)
        file = tk.Menu(men, tearoff=0)
        men.add_cascade(label="File", menu=file)
        file.add_command(label="Open…", accelerator="Ctrl+O", command=self.ask_open)
        file.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        file.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.save_as)
        file.add_separator()
        file.add_command(label="Exit", command=self.quit)
        self.bind_all("<Control-o>", lambda e: self.ask_open())
        self.bind_all("<Control-s>", lambda e: self.save())

        # horizontal paned window
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=4, bg="#1e222a")
        paned.pack(fill=tk.BOTH, expand=True)

        # left: plain-text editor
        self.text = st.ScrolledText(
            paned,
            wrap=tk.WORD,
            font=("Consolas", 13),
            undo=True,
            insertwidth=2,
            bg="#0f1115",
            fg="#e6e6e6",
            insertbackground="#e6e6e6",
            selectbackground="#264f78",
            selectforeground="#ffffff"
        )

        self.text.bind("<<Modified>>", self.on_edit)
        self.text.edit_modified(0)
        paned.add(self.text, stretch="always")

        # right: live preview (Chromium)
        self.preview = HtmlFrame(paned)
        paned.add(self.preview, stretch="always")

    # ---------- live markdown -> html ----------
    def on_edit(self, _event=None):
        src = self.text.get("1.0", tk.END)
        html_body = markdown.markdown(
            src,
            extensions=[
                "tables",
                "fenced_code",
                "codehilite",
                "toc",
                "md_in_html",
                "nl2br",
            ],
        )
        full_html = f"""<!doctype html><html><head><meta charset="utf-8">{CSS}</head>
                        <body>{html_body}</body></html>"""
        self.preview.load_html(full_html)  # show inside embedded browser
        self.text.edit_modified(0)

    # ---------- file I/O ----------
    def ask_open(self):
        f = fd.askopenfilename(filetypes=[("Markdown", "*.md *.markdown"), ("All", "*.*")])
        if f:
            self.open_file(pathlib.Path(f))

    def open_file(self, path: pathlib.Path):
        try:
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", path.read_text(encoding="utf-8"))
            self.file = path
            self.title(f"MDpad – {path.name}")
            self.on_edit()
        except Exception as e:
            mb.showerror("Open failed", str(e))

    def save(self):
        if self.file:
            self.file.write_text(self.text.get("1.0", tk.END), encoding="utf-8")
            self.text.edit_modified(0)
        else:
            self.save_as()

    def save_as(self):
        f = fd.asksaveasfilename(defaultextension=".md",
                                 filetypes=[("Markdown", "*.md"), ("All", "*.*")])
        if f:
            self.file = pathlib.Path(f)
            self.save()
            self.title(f"MDpad – {self.file.name}")

# ----------------------------------------------
# 4.  entry point
# ----------------------------------------------
if __name__ == "__main__":
    # support “Open with” from Explorer
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    MdPad(initial_file).mainloop()