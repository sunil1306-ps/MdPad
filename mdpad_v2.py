#!/usr/bin/env python3
"""
MDpad – a Notepad-like desktop app for Markdown
Beautiful live preview (Chromium inside Tkinter)
NEW: export to PDF / DOCX / HTML via pypandoc
"""
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.scrolledtext as st
import tkinter.messagebox as mb
import sys, pathlib, tempfile, webbrowser, textwrap, os
import markdown

# ------------------------------------------------------------------
# 0.  optional pypandoc – graceful degrade if missing
# ------------------------------------------------------------------
try:
    import pypandoc
    PANDOC_OK = True
except Exception:          # ImportError or PandocNotInstalled
    PANDOC_OK = False

# ------------------------------------------------------------------
# 1.  embedded browser pane (pip install tkinterweb)
# ------------------------------------------------------------------
try:
    from tkinterweb import HtmlFrame
except ImportError:
    mb.showerror("Missing package", "pip install tkinterweb")
    sys.exit(1)

# ------------------------------------------------------------------
# 2.  CSS that makes the preview beautiful
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# 3.  main application
# ------------------------------------------------------------------
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

        # File menu
        file = tk.Menu(men, tearoff=0)
        men.add_cascade(label="File", menu=file)
        file.add_command(label="Open…", accelerator="Ctrl+O", command=self.ask_open)
        file.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        file.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.save_as)

        # -------------- NEW: Export sub-menu --------------
        if PANDOC_OK:
            export = tk.Menu(file, tearoff=0)
            file.add_cascade(label="Export", menu=export)
            export.add_command(label="Export to PDF…", command=lambda: self.export_doc("pdf"))
            export.add_command(label="Export to DOCX…", command=lambda: self.export_doc("docx"))
            export.add_command(label="Export to standalone HTML…", command=lambda: self.export_doc("html"))
        else:
            file.add_command(label="Export (disabled – pypandoc / pandoc missing)", state="disabled")

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
        self.preview.load_html(full_html)
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

    # -------------- NEW: export via pypandoc --------------
    def export_doc(self, to_format: str):
        """Export current editor content to PDF/DOCX/HTML via pypandoc."""
        md_text = self.text.get("1.0", tk.END)
        if not md_text.strip():
            mb.showwarning("Nothing to export", "Editor is empty.")
            return

        # choose default filename and extension
        if self.file:
            default_name = self.file.with_suffix(f".{to_format}").name
        else:
            default_name = f"exported.{to_format}"

        f = fd.asksaveasfilename(
            defaultextension=f".{to_format}",
            filetypes=[(to_format.upper(), f"*.{to_format}"), ("All", "*.*")],
            initialfile=default_name
        )
        if not f:
            return  # user cancelled

        try:
            # pypandoc needs a temporary markdown file to read from
            with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tmp:
                tmp.write(md_text)
                tmp_name = tmp.name

            # PDF needs a little extra love (latex engine)
            extra_args = ["--pdf-engine=xelatex"] if to_format == "pdf" else []

            pypandoc.convert_file(
                tmp_name,
                to_format,
                outputfile=f,
                extra_args=extra_args
            )
            os.remove(tmp_name)  # tidy up
            mb.showinfo("Export complete", f"Saved to {f}")
        except Exception as e:
            mb.showerror("Export failed", str(e))


# ------------------------------------------------------------------
# 4.  entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    MdPad(initial_file).mainloop()