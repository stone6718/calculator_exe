import tkinter as tk
from tkinter import messagebox, scrolledtext, Menu
import sqlite3

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('calculations.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS calculations (expression TEXT, result TEXT)')
    conn.commit()
    conn.close()

def save_result(expression, result):
    conn = sqlite3.connect('calculations.db')
    c = conn.cursor()
    c.execute('INSERT INTO calculations (expression, result) VALUES (?, ?)', (expression, result))
    conn.commit()
    conn.close()

def fetch_records():
    conn = sqlite3.connect('calculations.db')
    c = conn.cursor()
    c.execute('SELECT expression, result FROM calculations')
    records = c.fetchall()
    conn.close()
    return records

def clear_records():
    conn = sqlite3.connect('calculations.db')
    c = conn.cursor()
    c.execute('DELETE FROM calculations')
    conn.commit()
    conn.close()
    messagebox.showinfo("초기화 완료", "모든 기록이 삭제되었습니다.")

def append_to_result(value):
    current_text = result_var.get()
    result_var.set(current_text + value)

def calculate():
    expression = result_var.get()
    try:
        result = str(eval(expression))
        result_var.set(result)
        save_result(expression, result)
    except Exception as e:
        messagebox.showerror("오류", "계산할 수 없습니다.")

def clear_result():
    result_var.set("")

def show_records():
    records = fetch_records()
    records_text = "\n".join([f"{expr} = {res}" for expr, res in records])
    
    # 스크롤 가능한 텍스트 박스에 기록 표시
    record_window = tk.Toplevel(root)
    record_window.title("저장된 기록")
    
    text_area = scrolledtext.ScrolledText(record_window, wrap=tk.WORD, width=40, height=30)
    text_area.insert(tk.END, records_text if records else "기록이 없습니다.")
    text_area.config(state=tk.DISABLED)  # 읽기 전용
    text_area.pack(padx=10, pady=10)

    close_button = tk.Button(record_window, text="닫기", command=record_window.destroy)
    close_button.pack(pady=5)

def show_support():
    messagebox.showinfo("설명", "해당 계산기는 오픈소스로 제작된 프로그램입니다.\n오픈소스를 사용할때 저작권자 표시 부탁드립니다.\nCC BY")

def show_copyright():
    messagebox.showinfo("저작권", "Copyright ⓒ 2024. NETCLOUD Co. All rights reserved.\ngithub @stone6718")

def create_menu():
    menu_bar = Menu(root)

    # 기록 메뉴
    record_menu = Menu(menu_bar, tearoff=0)
    record_menu.add_command(label="기록 보기", command=show_records)
    record_menu.add_command(label="데이터 초기화", command=clear_records)
    menu_bar.add_cascade(label="기록", menu=record_menu)

    # 도움말 메뉴
    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="설명", command=show_support)
    help_menu.add_command(label="저작권", command=show_copyright)
    menu_bar.add_cascade(label="도움말", menu=help_menu)

    root.config(menu=menu_bar)

# GUI 설정
init_db()

root = tk.Tk()
root.title("계산기")
result_var = tk.StringVar()

# UI 구성
entry = tk.Entry(root, textvariable=result_var, font=("Arial", 24), justify='right')
entry.grid(row=0, column=0, columnspan=4)

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

row_val = 1
col_val = 0

for button in buttons:
    if button == '=':
        btn = tk.Button(root, text=button, command=calculate, font=("Arial", 18))
    elif button == 'C':
        btn = tk.Button(root, text=button, command=clear_result, font=("Arial", 18))
    else:
        btn = tk.Button(root, text=button, command=lambda b=button: append_to_result(b), font=("Arial", 18))
    
    btn.grid(row=row_val, column=col_val, sticky='nsew', ipadx=10, ipady=10)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# 메뉴 생성
create_menu()

root.mainloop()