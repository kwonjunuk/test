import pandas as pd
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

file_path = r"C:\Users\wj123\OneDrive\문서\data.csv"

def analyze_shooting_pattern():
    data = pd.read_csv(file_path, header=None).iloc[:, 0]
    coords = {
        i: ((i-1) % 5, 4 - (i-1) // 5) for i in range(1, 26)
    }

    x_values = data.map(lambda x: coords[x][0])
    y_values = data.map(lambda x: coords[x][1])

    avg_coord = [sum(data.map(lambda x: coords[x][axis]))/len(data) for axis in [0, 1]]

    feedback = ""
    if abs(avg_coord[0]-2) < 1 and abs(avg_coord[1]-2) < 1:
        feedback = "명사수"
    else:
        if avg_coord[0] < 2:
            feedback += "좌"
        elif avg_coord[0] > 2:
            feedback += "우"
        if avg_coord[1] < 2:
            feedback += "하"
        elif avg_coord[1] > 2:
            feedback += "상"

        feedback += "측 편향"

    # 자세불량 판단
    x_variance = x_values.var()
    if x_variance > 1:  # 임의의 임계값을 1로 설정하였으나, 필요에 따라 조정 가능
        feedback += "\n자세불량"

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x_values, y_values, c='blue', label='Shots')
    ax.scatter(avg_coord[0], avg_coord[1], c='red', marker='x', label='Average')
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.grid(True)
    ax.set_title("Shooting Pattern")
    ax.set_xlabel("X (Target)")
    ax.set_ylabel("Y (Target)")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, padx=10, pady=10)
    plt.close(fig)

    return feedback

def shooting_analysis():
    feedback = analyze_shooting_pattern()
    messagebox.showinfo("피드백", feedback)

root = tk.Tk()
root.title("사격 분석")

analyze_btn = tk.Button(root, text="사격 분석 시작", command=shooting_analysis)
analyze_btn.grid(row=1, column=0, pady=10)

root.mainloop()
