import threading
from utils import getGptResponse
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
def save_file(event, text):
    file_path = ttk.filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text.get(1.0, ttk.END))


def createGptTranslatePage(root, text, icon_path):
    main_text = text.get(1.0, ttk.END)
    gpt_page = ttk.Toplevel(root)
    new_font = ttk.font.Font(family="Microsoft YaHei", size=12)
    gpt_page.title("GPT例句产生器")
    gpt_page.iconbitmap(icon_path)
    menu_bar = ttk.Menu(gpt_page)
    file_menu = ttk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="保存", accelerator="Ctrl+s",
                          command=lambda: save_file(None, gpt_text))
    gpt_page.config(menu=menu_bar)

    label = ttk.Label(
        gpt_page,text="欢迎来到gpt例句产生器！😊\n点击下面的按钮就可以获取例句了，需要加载几秒，具体时间取决于你的单词和翻译数量，请耐心等待，祝使用愉快！")
    label.pack()
    gpt_text = ttk.Text(gpt_page, wrap=ttk.WORD)
    gpt_text.configure(font=new_font)
    gpt_text.pack(expand=True, fill=ttk.BOTH)
    gpt_text.bind("<Control-s>", lambda event: save_file(event, gpt_text))
    gpt_text.bind("<Control-S>", lambda event: save_file(event, gpt_text))

    def update_gpt_gui(chunk_message):
        def insert_text(chunk_message):
            gpt_text.insert(ttk.END, chunk_message)
            gpt_text.see(ttk.END)  # Scroll to the new message
            gpt_page.update_idletasks()  # Update the GUI
        gpt_text.after(0, lambda: insert_text(chunk_message))

    def generateResp():
        getGptResponse(main_text, update_gpt_gui)
    translate_button = ttk.Button(
        gpt_page, text="点击获取主页面单词所有例句", bootstyle=SUCCESS, command=lambda: threading.Thread(target=generateResp).start())
    translate_button.pack(padx=5, pady=10)
