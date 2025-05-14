import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def main_menu(root, user_number):
    from settings import settings_window
    from quiz_menu import quiz_menu
    from vocab import vocab_window


    def open_vocab():
        vocab_window(root, user_number)

    def open_quiz():
        quiz_menu(root, user_number)

    def open_settings():
        settings_window(root, user_number)


    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()

    root.title("메인 메뉴")
    root.geometry("320x400")

    title_label = ttk.Label(root, text="메인 메뉴", font=("Arial", 18, "bold"), bootstyle="primary")
    title_label.pack(pady=20)

    vocab_button = ttk.Button(root, text="단어장", bootstyle="success", command=open_vocab, width=20)
    vocab_button.pack(pady=10, padx=10)

    quiz_button = ttk.Button(root, text="퀴즈", bootstyle="info", command=open_quiz, width=20)  # 수정된 부분
    quiz_button.pack(pady=10, padx=10)

    settings_button = ttk.Button(root, text="설정", bootstyle="warning", command=open_settings, width=20)
    settings_button.pack(pady=10, padx=10)

    exit_button = ttk.Button(root, text="종료", bootstyle="danger", command=root.quit)
    exit_button.pack(side= "bottom", pady=20)


