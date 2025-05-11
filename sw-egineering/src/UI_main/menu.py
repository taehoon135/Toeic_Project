import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def main_menu(root, app):
    from settings import settings_window
    from quiz_menu import quiz_menu
    from vocab import vocab_window

    def open_vocab():
        vocab_window(root, app)

    def open_quiz():
        quiz_menu(root, app)

    def open_settings():
        settings_window(root, app)

    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()

    root.title("메인 메뉴")
    root.geometry("400x500")

    # 사용자 정보 표시
    if app.get_current_user():
        user = app.get_current_user()
        user_label = ttk.Label(root, 
                             text=f"환영합니다, {user['user_name']}님!", 
                             font=("Arial", 12),
                             bootstyle="info")
        user_label.pack(pady=10)

    title_label = ttk.Label(root, text="메인 메뉴", font=("Arial", 18, "bold"), bootstyle="primary")
    title_label.pack(pady=20)

    vocab_button = ttk.Button(root, text="단어장", bootstyle="success", command=open_vocab)
    vocab_button.pack(pady=10, fill=X, padx=50)

    quiz_button = ttk.Button(root, text="퀴즈", bootstyle="info", command=open_quiz)
    quiz_button.pack(pady=10, fill=X, padx=50)

    settings_button = ttk.Button(root, text="설정", bootstyle="warning", command=open_settings)
    settings_button.pack(pady=10, fill=X, padx=50)

    exit_button = ttk.Button(root, text="종료", bootstyle="danger", command=root.quit)
    exit_button.pack(pady=20)


