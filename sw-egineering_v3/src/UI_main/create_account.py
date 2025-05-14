import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

def register(root):
    #순환참조 방지
    from login import sign_login

    #DB연결
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
    from database.user_db import UserDB

    user_db = UserDB() #클래스 생성

    def set_placeholder(entry_widget, placeholder_text, is_password=False):
        """입력 필드에 플레이스홀더를 설정 (비밀번호 필드 대응)"""
        entry_widget.insert(0, placeholder_text)
        entry_widget.has_placeholder = True  
        entry_widget.config(style="Placeholder.TEntry")  

        def on_focus_in(event):
            if entry_widget.has_placeholder:
                entry_widget.delete(0, tk.END)
                entry_widget.config(style="Normal.TEntry")  
                if is_password:
                    entry_widget.config(show="*")  
                entry_widget.has_placeholder = False  

        def on_focus_out(event):
            if not entry_widget.get().strip():  
                entry_widget.insert(0, placeholder_text)
                entry_widget.config(style="Placeholder.TEntry")  
                if is_password:
                    entry_widget.config(show="")  
                entry_widget.has_placeholder = True  

        entry_widget.bind("<FocusIn>", on_focus_in)
        entry_widget.bind("<FocusOut>", on_focus_out)

    def back_to_login():
        sign_login(root)

    def sign_register(id, password, comfirm_password, name, phone_number):
        if (id.has_placeholder or id.get().strip() == ""):
            messagebox.showwarning("경고", "아이디가 입력되지 않았습니다.")
            return
        if (password.has_placeholder or password.get().strip() == ""):
            messagebox.showwarning("경고", "비밀번호가 입력되지 않았습니다.")
            return
        if (comfirm_password.has_placeholder or comfirm_password.get().strip() == ""):
            messagebox.showwarning("경고", "비밀번호가 입력되지 않았습니다.")
            return
        if (name.has_placeholder or name.get().strip() == ""):
            messagebox.showwarning("경고", "이름이 입력되지 않았습니다.")
            return
        if (phone_number.has_placeholder or phone_number.get().strip() == ""):
            messagebox.showwarning("경고", "전화번호가 입력되지 않았습니다.")
            return
        if (password.get() != comfirm_password.get()):
            messagebox.showwarning("경고", "비밀번호가 일치하지 않습니다.")
            return

        #비밀번호가 일치하면 데이터베이스에 항목 추가
        #user_login_id, user_pw, user_name, is_admin=0, user_api=None
        if (password.get() == comfirm_password.get()):
            id_num = user_db.register_user(id.get(), password.get(), name.get())
            print(id_num, id.get(), password.get())
            messagebox.showinfo("성공", "회원가입이 완료되었습니다!")
            back_to_login()
        else:
            print("문제 발생")

    def switch_to_signup():
        """로그인 UI 제거 후 회원가입 UI 표시"""
        for widget in root.winfo_children():
            widget.destroy()  

        # 뒤로가기 버튼 (오른쪽 상단)
        back_button = ttk.Button(root, text="← 뒤로", bootstyle="secondary", command=back_to_login)
        back_button.pack(anchor="ne", padx=10, pady=10)

        # 회원가입 제목
        title_label = ttk.Label(root, text="회원가입", font=("Arial", 18, "bold"), bootstyle="primary")
        title_label.pack(pady=10)

        # 아이디 입력
        id_entry = ttk.Entry(root, width=30, bootstyle="info", style="Placeholder.TEntry")
        id_entry.pack(pady=5)
        set_placeholder(id_entry, "ID")

        # 비밀번호 입력
        password_entry = ttk.Entry(root, width=30, bootstyle="info", style="Placeholder.TEntry")
        password_entry.pack(pady=5)
        set_placeholder(password_entry, "Password", is_password=True)

        # 비밀번호 확인 입력
        confirm_password_entry = ttk.Entry(root, width=30, bootstyle="info", style="Placeholder.TEntry")
        confirm_password_entry.pack(pady=5)
        set_placeholder(confirm_password_entry, "Confirm Password", is_password=True)

        # 이름 입력
        name_entry = ttk.Entry(root, width=30, bootstyle="info", style="Placeholder.TEntry")
        name_entry.pack(pady=5)
        set_placeholder(name_entry, "Name")

        # 전화번호 입력
        phone_entry = ttk.Entry(root, width=30, bootstyle="info", style="Placeholder.TEntry")
        phone_entry.pack(pady=5)
        set_placeholder(phone_entry, "Phone Number")

        #엔터키로 입력
        id_entry.bind("<Return>", lambda event: sign_register(id_entry, password_entry, confirm_password_entry, name_entry, phone_entry))
        password_entry.bind("<Return>", lambda event: sign_register(password_entry, password_entry, confirm_password_entry, name_entry, phone_entry))
        confirm_password_entry.bind("<Return>", lambda event: sign_register(password_entry, password_entry, confirm_password_entry, name_entry, phone_entry))
        name_entry.bind("<Return>", lambda event: sign_register(name_entry, password_entry, confirm_password_entry, name_entry, phone_entry))
        phone_entry.bind("<Return>", lambda event: sign_register(id_entry, password_entry, confirm_password_entry, name_entry, phone_entry))

        # 회원가입 버튼 (양쪽 여백 추가)
        signup_button = ttk.Button(root, text="회원가입", bootstyle="success", command=lambda: sign_register(id_entry, password_entry, confirm_password_entry,name_entry, phone_entry))
        signup_button.pack(pady=10, padx=100, fill=X)

    switch_to_signup()  # 초기 UI 표시
