from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
from sentence_gpt import createGptTranslatePage
from utils import fetch_youdao_definition

def fetch_and_display_definition(word):
    definition = fetch_youdao_definition(word)
    if definition:
        text.insert("insert lineend", f"\t{definition}\n")


def on_enter(event):
    current_line = text.get("insert linestart", "insert lineend").strip()
    fetch_and_display_definition(current_line)


def show_about():
    messagebox.showinfo(title='关于',
                        message=f'版本: version 1.0\n作者:meowrain\n使用方法:在文本框内输入单词然后回车，会自动在这个单词后面加载这个单词的释义\n加入QQ群了解更多：887940241')


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text.delete(1.0, ttk.END)
            text.insert(ttk.END, file.read())


def save_file(event):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text.get(1.0, ttk.END))


def exit():
    root.quit()


def change_to_darkly_theme():
    style.theme_use('darkly')


def change_to_default_theme():
    style.theme_use('cosmo')


if __name__ == '__main__':

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    icon_path = os.path.join(script_dir, "favicon.ico")
    root = ttk.Window(title="单词翻译器", themename="darkly")
    style = ttk.Style('darkly')
    text = ttk.Text(root, wrap=ttk.WORD)
    new_font = ttk.font.Font(family="Microsoft YaHei", size=12)
    text.configure(font=new_font)
    text.pack(expand=True, fill=ttk.BOTH)
    text.bind("<Return>", on_enter)
    menu_bar = ttk.Menu(root)
    root.config(menu=menu_bar)
    file_menu = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="文件", menu=file_menu)
    theme_menu = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="主题", menu=theme_menu)
    theme_menu.add_command(label="夜间模式", command=change_to_darkly_theme)
    theme_menu.add_command(label="白天模式", command=change_to_default_theme)
    menu_bar.add_command(
        label="gpt例句", command=lambda: createGptTranslatePage(root, text, icon_path))
    menu_bar.add_command(label="关于", command=show_about)
    file_menu.add_command(label="打开", command=open_file)
    file_menu.add_command(label="保存", accelerator="Ctrl+s",
                          command=lambda: save_file(None))
    file_menu.add_command(label="退出", command=exit)
    text.bind("<Control-s>", save_file)
    text.bind("<Control-S>", save_file)
    root.mainloop()
