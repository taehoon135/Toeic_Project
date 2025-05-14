import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

def quiz_four_choice(root1):
    from quiz_result import quiz_result

    word_list = [
        ["cold", "추운", 0, "카테고리1"],
        ["home", "집", 0, "전체"],
        ["school", "학교", 1, "전체"],
        ["mission", "임무", 0, "전체"],
        ["hot", "뜨거운", 2, "카테고리2"],
        ["happy", "행복한", 0, "전체"]
    ]
    word_list_anwser = [0 for _ in range(len(word_list))]

    def enter():  #정답 여부 저장
        nonlocal current_index
        selected_word = var.get()
        
        if selected_word == word_list[current_index][0]:
            word_list_anwser[current_index] = 1
        else:
            word_list_anwser[current_index] = 0
            word_list[current_index][2] += 1 
        
        current_index += 1
        next_word()

    def next_word():
        nonlocal current_index

        if (current_index >= len(word_list_anwser)):
            messagebox.showinfo("", "모든 단어를 완료했습니다!")
            quiz_result(root1, word_list, word_list_anwser)
        else:
            word_label.config(text=word_list[current_index][1], font=("Arial", 25))  #문제 갱신
            count_word.config(text=f"남은 단어 갯수: {len(word_list) - current_index}", font=("나눔 고딕", 16))  #남은 단어 갯수 갱신
            var.set(None)  #이전 선택 초기화

            # 체크박스 옵션 갱신
            options = [word_list[current_index][0]]  #보기 안에 정답이 존재해야 하므로 정답먼저 리스트에 추가
            while len(options) < 4:  #보기 개수를 4개로 조절
                other = random.choice(word_list)[0]
                if other not in options:  #중복된 단어가 보기로 들어가지 않게 조절함
                    options.append(other)
            random.shuffle(options) # 보기 순서를 랜덤으로 섞음
            for i in range(4):
                checkboxes[i].config(text=options[i], variable=var, value=options[i])

                # text=options[i] 	Radiobutton의 **라벨(보기로 표시될 텍스트)**을 options[i]로 설정
                # variable=var	    사용자가 선택한 값을 저장할 변수 (StringVar() 타입)
                # value=options[i]	해당 버튼을 선택했을 때 var에 저장될 값


    #윈도우 초기화 과정
    current_index = 0
    root1.geometry("500x400")
    for widget in root1.winfo_children():
        widget.destroy()  
    
    tk.Label(root1, text="정답을 선택하세요", font=("나눔 고딕", 16)).pack(pady=20)
    word_label = tk.Label(root1, text=word_list[current_index][1], font=("Arial", 25))
    word_label.pack(pady=15)

    var = tk.StringVar()  #사용자가 선택했을때 저장될 공간
    var.set(None)  #체크박스 비우기
    checkboxes = []  #체크박스 옆에 보여줄 보기들

    frame = tk.Frame(root1)
    frame.pack(pady=10)

    for i in range(4):
        cb = tk.Radiobutton(frame, text=f"", variable=var, value=f"", font=("나눔 고딕", 14), indicatoron=0, width=10, height=2, relief="raised")  #랜덤으로 뽑아야 하기에 처음에는 비워둠
        cb.grid(row=i // 2, column=i % 2, padx=10, pady=5)
        checkboxes.append(cb)  #나중에 조작할 수 있도록 저장하는 역할
    
    submit_button = tk.Button(root1, text="확인", command=enter, width=15, height=2)
    submit_button.pack(pady=20)
    root1.bind("<Return>", lambda event: enter())
    
    count_word = tk.Label(root1, text=f"남은 단어 갯수: {len(word_list) - current_index}", font=("나눔 고딕", 16))
    count_word.pack(side="bottom", pady=5)

    next_word()  #시작
