import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from login import sign_login

# 현재 테마 상태 변수
current_theme = "flatly"  # 기본 테마 (라이트 모드)

# 메인 윈도우 생성 (ttkbootstrap 테마 적용)
root = ttk.Window(themename=current_theme)  # 초기 테마: flatly (라이트 모드)
root.title("영단어 학습 프로그램")
root.geometry("320x400")  # 높이 조정
root.resizable(False, False)

# 스타일 설정 (회색 플레이스홀더 스타일 추가)
style = ttk.Style()
style.configure("Placeholder.TEntry", foreground="gray")
style.configure("Normal.TEntry", foreground="black")

sign_login(root)

# 메인 루프 실행
root.mainloop()
