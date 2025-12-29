# tkhtml.py  –  public-domain, ultra-minimal HTML viewer for Tk
import tkinter as tk, tkinter.font, html, re, urllib.parse

class HtmlFrame(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master)
        self.text = tk.Text(self, wrap=tk.WORD, **{k: kw.pop(k) for k in list(kw) if k in
                   {'width','height','bg','fg','font','padx','pady','cursor'}})
        vs = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=vs.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vs.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(state=tk.DISABLED)

    def set_content(self, html_src):
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self._insert_html(html_src)
        self.text.config(state=tk.DISABLED)

    # very small subset: <p>, <br>, <h1>..<h6>, <b>, <i>, <code>, <pre>, <a>
    def _insert_html(self, src):
        plain = re.sub(r'<br\s*/?>', '\n', src, flags=re.I)
        plain = re.sub(r'<p>', '\n\n', plain, flags=re.I)
        plain = re.sub(r'</?p>', '', plain, flags=re.I)
        tags = re.finditer(r'<(/?)(h[1-6]|b|i|code|pre|a)(?:[^>]*)>', plain, re.I)
        stack, start, out = [], 0, []
        font = tk.font.nametofont(self.text.cget('font'))
        for m in tags:
            out.append(plain[start:m.start()])
            tag, name = m.group(1).lower(), m.group(2).lower()
            if tag:  # closing
                if stack and stack[-1][0] == name:
                    stack.pop()
            else:    # opening
                stack.append((name, m.end()))
            start = m.end()
        out.append(plain[start:])
        self.text.insert(tk.END, ''.join(out))
        # apply simple formatting
        for name, idx in stack:
            if name == 'h1': self.text.tag_add('h1', f'1.0+{idx}c', tk.END)
        self.text.tag_configure('h1', font=(font.actual('family'), int(font.actual('size')*2), 'bold'))