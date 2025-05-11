import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from login import sign_login
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from database.user_db import UserDB

class App:
    def __init__(self):
        self.user_db = UserDB()
        self.current_user = None
        self.current_theme = "flatly"  # 기본 테마 (라이트 모드)
        
        # 메인 윈도우 생성
        self.root = ttk.Window(themename=self.current_theme)
        self.root.title("영단어 학습 프로그램")
        self.root.geometry("320x400")
        self.root.resizable(False, False)
        
        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure("Placeholder.TEntry", foreground="gray")
        self.style.configure("Normal.TEntry", foreground="black")
        
        # 로그인 화면 표시
        sign_login(self.root, self)
        
    def run(self):
        """앱 실행"""
        self.root.mainloop()
        
    def set_current_user(self, user):
        """현재 로그인한 사용자 설정"""
        self.current_user = user
        
    def get_current_user(self):
        """현재 로그인한 사용자 정보 반환"""
        return self.current_user
        
    def change_theme(self, theme_name):
        """테마 변경"""
        self.current_theme = theme_name
        self.root.style.theme_use(theme_name)

if __name__ == "__main__":
    app = App()
    app.run()
