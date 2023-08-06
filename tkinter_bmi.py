import tkinter as tk
from tkinter import messagebox

def CalculateMBI():
    kg = int(weight_ent.get())
    m = int(height_ent.get()) / 100
    bmi = kg / m**2
    bmi = round(bmi, 1)
    print(bmi)
    if bmi <= 18.5:
        messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует недостаточному весу')
    elif (bmi > 18.5) and (bmi <= 24.9):
        messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует нормальному весу')
    elif (bmi > 24.9) and (bmi < 29.9):
        messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует избыточному весу')
    else:
        messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует ожирению')
window = tk.Tk()
window.title("Калькулятор индекса массы тела (ИМТ)")
window.geometry('800x600') # size

frame = tk.Frame(
   window,
   padx=10,
   pady=10
)
frame.pack(expand=True)

height_lb = tk.Label(
   frame,
   text="Введите свой рост (в см)  "
)
height_lb.grid(row=3, column=1)

weight_lb = tk.Label(
    frame,
    text="Введите свой вес (в кг)  "
)
weight_lb.grid(row=4, column=1)

height_ent = tk.Entry(
   frame
)
height_ent.grid(row=3, column=2)

weight_ent = tk.Entry(
    frame
)
weight_ent.grid(row=4, column=2, pady=5)

button = tk.Button(
    frame,
    text="Рассчитать ИМТ",
    command=CalculateMBI
)
button.grid(row=5, column=2, pady=5)

window.mainloop()