import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox, font
from tkinter import PhotoImage

def category_manage(root):
    from vocab import vocab_window
    from category_make import category_make

    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()

    #뒤로가기
    def go_to_menu():
        vocab_window(root)

    #카테고리 생성
    def go_to_make_category():
        category_make(root)

    #마지막으로 선택된 트리뷰 구분
    last_selected_tree = None

    #카테고리 삭제
    def delete_category():
        selected = category_table.focus()
        data = category_table.item(selected, "values")

        # if not selected:
        #     messagebox.showwarning("선택 오류", "삭제할 카테고리를 선택하세요.")
        #     return
        
        confirm = messagebox.askyesno("카테고리 삭제", "정말로 삭제하시겠습니까?")
        if confirm:
            print(data[0] + " 카테고리 삭제")
            update_word_table() #카테고리 목록 초기화
            #선택된 트리뷰 초기화
            nonlocal last_selected_tree
            last_selected_tree = None
        else:
            return
        
    #카테고리 내의 단어 삭제
    def delete_word_in_category():
        #카테고리 데이터
        selected = category_table.focus()
        data = category_table.item(selected, "values")
        #카테고리에 속한 단어 데이터
        selected_word = word_table.focus()
        data_word = word_table.item(selected_word, "values")

        # if not selected_word:
        #     messagebox.showwarning("선택 오류", "삭제할 단어를 선택하세요.")
        #     return
        
        confirm = messagebox.askyesno("단어 삭제", "정말로 삭제하시겠습니까?")
        if confirm:
            print(data[0] + " 카테고리의 " + data_word[0] + " 단어 삭제")
            update_word_table() #카테고리 목록 초기화
            #선택된 트리뷰 초기화
            nonlocal last_selected_tree
            last_selected_tree = None
        else:
            return
        
    def category_or_word(category_table, word_table):
        nonlocal last_selected_tree
        if (last_selected_tree == None):
            messagebox.showwarning("선택 오류", "아무것도 선택되지 않음.")
        elif (last_selected_tree == category_table):
            delete_category()
        elif (last_selected_tree == word_table):
            delete_word_in_category()
        
    #예시
    category_word = [
        ["fruit", 3,"apple", "사과", "banana", "바나나", "blueberry", "블루베리"],
        ["cant_remember", 2, "fight", "싸우다", "tiger", "호랑이"],
        ["language", 1, "english", "영어"]
    ]

    # 단어 테이블 업데이트
    def update_word_table():
        for row in category_table.get_children(): #기존 카테고리 목록 삭제
            category_table.delete(row)
        for item in category_word:
            category_table.insert("", "end", values=(item[0], item[1])) #카테고리 새로 다시 업데이트
        for row2 in word_table.get_children():
            word_table.delete(row2)

    #treeview를 클릭했을때의 처리
    def on_row_click(event):
        nonlocal last_selected_tree
        selected_tree = event.widget
        selected_item = selected_tree.focus()
        data = selected_tree.item(selected_item, "values")

        #마지막으로 카테고리가 선택된 경우
        if selected_tree == category_table and selected_item:
            last_selected_tree = category_table

            #data에는 카테고리와 단어 갯수밖에 없으므로 원래 리스트에서 다시 찾기
            for index in range(len(category_word)):
                if (category_word[index][0] == data[0]):
                    break

            #기존 목록 삭제
            for row in word_table.get_children():
                word_table.delete(row)
            #카테고리에 소속된 단어 밑 트리뷰에 출력
            for i in range(int(category_word[index][1])):
                category_index = i * 2
                word_table.insert("", "end", values=(category_word[index][category_index+2], category_word[index][category_index+3])) #짝수번째는 영단어, 홀수번째는 뜻

        #마지막으로 카테고리 내의 단어가 선택된 경우
        elif (selected_tree == word_table and selected_item):
            last_selected_tree = word_table

    # GUI 시작
    root.geometry("500x600")

    # ===== 폰트 설정 =====
    big_font = font.Font(family="맑은 고딕", size=13)
    tree_font = font.Font(family="맑은 고딕", size=13)

    # ===== 스타일 설정 =====
    style = ttk.Style()
    style.configure("Custom.Treeview", font=tree_font, rowheight=32)
    style.configure("Big.TButton", font=big_font)

    # 상단바 (카테고리 생성 + 뒤로가기)
    top_bar = ttk.Frame(root)
    top_bar.pack(fill=tk.X, pady=5, padx=10)

    #카테고리 생성 버튼
    category_make_button = ttk.Button(top_bar, text="카테고리 생성", command=go_to_make_category, style="Big.TButton")
    category_make_button.pack(side=tk.LEFT)

    #뒤로가기 버튼
    back_button = ttk.Button(top_bar, text="← 뒤로가기", command=go_to_menu, style="Big.TButton")
    back_button.pack(side=tk.RIGHT)

    # 카테고리 테이블
    table_frame = ttk.Frame(root)
    table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

    columns = ("category_name", "a_number_of_word")
    category_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12, style="Custom.Treeview") 
    category_table.heading("category_name", text="카테고리")
    category_table.heading("a_number_of_word", text="저장된 단어 갯수")
    category_table.column("category_name", width=100, anchor="center")
    category_table.column("a_number_of_word", width=100, anchor="center")
    category_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    category_table.bind("<<TreeviewSelect>>", on_row_click)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=category_table.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    category_table.configure(yscrollcommand=scrollbar.set)

    #카테고리 별 저장된 단어 목록
    word_for_category_frame = ttk.Frame(root)
    word_for_category_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    columns_word = ("word", "meaning")
    word_table = ttk.Treeview(word_for_category_frame, columns=columns_word, show="headings", height=12, style="Custom.Treeview")
    word_table.heading("word", text="단어")
    word_table.heading("meaning", text="뜻")
    word_table.column("word", width=100, anchor="center")
    word_table.column("meaning", width=100, anchor="center")
    word_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    word_table.bind("<<TreeviewSelect>>", on_row_click)
    
    scrollbar = ttk.Scrollbar(word_for_category_frame, orient="vertical", command=word_table.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    word_table.configure(yscrollcommand=scrollbar.set)

    #삭제 버튼을 젤 밑으로 내리기 위한 바텀 프레임
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(fill=tk.X, padx=10, pady=10)

    #삭제 버튼
    delete_button = ttk.Button(bottom_frame, text="삭제", style="Big.TButton", command=lambda: category_or_word(category_table, word_table))
    delete_button.pack(anchor="e")

    # 초기 카테고리 표시
    update_word_table()