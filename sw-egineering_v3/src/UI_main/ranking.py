from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def ranking(root, user_number):
    # 메인 메뉴 함수 import
    from quiz_menu import quiz_menu

    # 기존 창의 모든 위젯 제거 (화면 초기화)
    for widget in root.winfo_children():
        widget.destroy()

    # 창 크기 설정
    root.geometry("500x600")

    # '메인 메뉴' 버튼 클릭 시 실행되는 함수
    def go_to_quiz_menu():
        quiz_menu(root, user_number)

    user_info = ["3", "john", "300"]
    user_rank = [["1", "pohn", "990"], ["2", "kim", "800"], ["3", "john", "300"], ["4", "miss", "10"]]

    #사용자 정보와 뒤로가기 프레임 생성
    user_frame = ttk.Frame(root, borderwidth=2, relief="solid", padding=1)
    user_frame.place(x=5, y=10, width=200, height=50)

    info_label = ttk.Label(user_frame, text= "사용자 ID: " + user_info[1][: 15], font=("Arial", 11))
    info_label.pack(anchor="w")
    rank_label = ttk.Label(user_frame, text= "현재순위: " + user_info[0] + "위", font=("Arial", 11))
    rank_label.pack(anchor="w")

    # '메인 메뉴' 버튼 생성 및 배치
    exit_btn = ttk.Button(root, text="뒤로가기", bootstyle="success", command=go_to_quiz_menu)
    exit_btn.pack(anchor="e", padx=10, pady=10)

    # 결과를 표시할 프레임 생성 및 배치
    result_frame = ttk.Frame(root)
    result_frame.place(x=10, y=80, width=480, height=500)

    # Treeview에 표시할 컬럼 정의 ('mistakes'는 제거됨)
    columns = ("순위", "사용자ID", "최고점수")

    # Treeview 스타일 설정 (선택 시 파란색 배경 제거)
    style = ttk.Style()
    style.configure("Custom.Treeview", highlightthickness=0, bd=0, font=('Arial', 10))
    style.configure("Custom.Treeview.Heading", font=('Arial', 10, 'bold'))
    style.map("Custom.Treeview", background=[("selected", "white")], foreground=[("selected", "black")])

    # Treeview 위젯 생성
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=20, style="Custom.Treeview")

    # 각 컬럼의 헤더와 너비 설정
    for col, width in zip(columns, [100, 100, 100]):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="center")

    # Treeview 배치
    tree.pack(side="left", fill="both", expand=True)

    # 스크롤바 생성 및 Treeview에 연결
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Treeview에 단어 데이터 삽입
    for i, (rank, userID, point) in enumerate(user_rank):
        tree.insert("", "end", iid=i, values=(rank, userID, point))