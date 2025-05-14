import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# def quiz_result(root, word_list, word_list_answer):

#     for widget in root.winfo_children():
#             widget.destroy()  

#     # 마우스 휠 스크롤 이벤트 함수
#     def on_mouse_wheel(event):
#         canvas.yview_scroll(-1 * (event.delta // 120), "units")

#     root.geometry("600x600")

#     # 결과 프레임 (스크롤 포함)
#     result_frame = tk.Frame(root, bg="white", relief="solid", bd=1)
#     result_frame.place(x=20, y=20, width=550, height=500)

#     canvas = tk.Canvas(result_frame, bg="white")
#     scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)

#     scrollable_frame = tk.Frame(canvas, bg="white")
#     scrollable_frame.bind(
#         "<Configure>",
#         lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#     )

#     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#     canvas.configure(yscrollcommand=scrollbar.set)

#     canvas.pack(side="left", fill="both", expand=True)
#     scrollbar.pack(side="right", fill="y")

#     # 마우스 휠 스크롤 이벤트 바인딩
#     root.bind("<MouseWheel>", on_mouse_wheel)


#     #카테고리 선택값을 저장할 리스트
#     category_vars = []

#     def go_to_main_menu():
#         #선택된 카테고리 별로 단어들을 저장함
#         for i, (word, meaning, mistakes, category) in enumerate(word_list):
#              print(word + "의 카테고리: " + category_vars[i].get())

#         root.quit()
#         #main_menu(root)

#     # 카테고리 리스트를 데이터베이스에서 받았다고 가정
#     categories = ["전체", "카테고리2", "카테고리3", "카테고리4"]

#     # 단어 리스트 출력
#     for i, (word, meaning, mistakes, category) in enumerate(word_list):

#         category_var = tk.StringVar()
#         category_var.set(categories[0])  # 기본 선택값을 명시적으로 설정
#         category_vars.append(category_var)

#         category_menu = ttk.OptionMenu(scrollable_frame, category_var, categories[0], *categories)
#         category_menu.grid(row=i, column=0, padx=12, pady=5)
        
#         # 단어 (조금 오른쪽으로 이동)
#         tk.Label(scrollable_frame, text=word, width=15, anchor="center", bg="white", font=("Arial", 10)).grid(row=i, column=1, padx=15, pady=5)
        
#         # 단어 해석
#         tk.Label(scrollable_frame, text=meaning, width=10, anchor="center", bg="white", font=("Arial", 10)).grid(row=i, column=2, padx=5, pady=5)
        
#         # 오답 횟수
#         tk.Label(scrollable_frame, text=f"{mistakes}회", width=5, anchor="center", bg="white", font=("Arial", 10)).grid(row=i, column=3, padx=5, pady=5)
        
#         # 정답 여부 (O/X)
#         if (word_list_answer[i] == 1): #맞춘 케이스
#             correctness_label = tk.Label(scrollable_frame, text="O", width=5, anchor="center", bg="white", font=("Arial", 10, "bold"))
#             correctness_label.grid(row=i, column=4, padx=5, pady=5)
#         elif (word_list_answer[i] == 0): #틀린 케이스
#             correctness_label = tk.Label(scrollable_frame, text="X", width=5, anchor="center", bg="white", font=("Arial", 10, "bold"))
#             correctness_label.grid(row=i, column=4, padx=5, pady=5)

#     # 종료 버튼
#     exit_btn = ttk.Button(root, text="메인 메뉴", bootstyle="success", command=go_to_main_menu)
#     exit_btn.place(x=480, y=540)


def quiz_result(root, word_list, word_list_answer):
    # 메인 메뉴 함수 import
    from menu import main_menu

    # 기존 창의 모든 위젯 제거 (화면 초기화)
    for widget in root.winfo_children():
        widget.destroy()

    # 창 크기 설정
    root.geometry("500x600")

    # 결과를 표시할 프레임 생성 및 배치
    result_frame = ttk.Frame(root)
    result_frame.place(x=10, y=20, width=480, height=500)

    # Treeview에 표시할 컬럼 정의 ('mistakes'는 제거됨)
    columns = ("Sentence", "Word", "correctness")

    # Treeview 스타일 설정 (선택 시 파란색 배경 제거)
    style = ttk.Style()
    style.configure("Custom.Treeview", highlightthickness=0, bd=0, font=('Arial', 10))
    style.configure("Custom.Treeview.Heading", font=('Arial', 10, 'bold'))
    style.map("Custom.Treeview", background=[("selected", "white")], foreground=[("selected", "black")])

    # Treeview 위젯 생성
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=20, style="Custom.Treeview")

    # 각 컬럼의 헤더와 너비 설정
    for col, width in zip(columns, [110, 110, 80]):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="center")

    # Treeview 배치
    tree.pack(side="left", fill="both", expand=True)

    # 스크롤바 생성 및 Treeview에 연결
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Treeview에 단어 데이터 삽입
    for i, (word, meaning, _, _) in enumerate(word_list):
        correctness = "O" if word_list_answer[i] == 1 else "X"  # 정답 여부 표시
        tree.insert("", "end", iid=i, values=(word, meaning, correctness))

    # '메인 메뉴' 버튼 클릭 시 실행되는 함수
    def go_to_main_menu():
        main_menu(root)

    # '메인 메뉴' 버튼 생성 및 배치
    exit_btn = ttk.Button(root, text="메인 메뉴", bootstyle="success", command=go_to_main_menu)
    exit_btn.place(x=370, y=540)