import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customexceptions import InvalidInputException
from sleepnote import SleepEntry

# основной класс
class SleepTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для отслеживания сна")

        # список записей сна
        self.sleep_entries = []

        # создание окна с польз. интерфейсрм
        self.create_widgets()

    def create_widgets(self):
        # ввод данных
        tk.Label(self.root, text="Дата (дд-мм-гггг)").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Время начала сна (чч:мм)").grid(row=1, column=0)
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Время окончания сна (чч:мм)").grid(row=2, column=0)
        self.end_time_entry = tk.Entry(self.root)
        self.end_time_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Комментарий").grid(row=3, column=0)
        self.comment_entry = tk.Entry(self.root)
        self.comment_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2)

        # таблица записей
        self.tree = ttk.Treeview(self.root, columns=("date", "start", "end", "duration", "comment"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("start", text="Начало")
        self.tree.heading("end", text="Окончание")
        self.tree.heading("duration", text="Длительность (ч)")
        self.tree.heading("comment", text="Комментарий")
        self.tree.grid(row=5, column=0, columnspan=2)

        # логи
        tk.Label(self.root, text="Лог действий").grid(row=6, column=0)
        self.log_text = tk.Text(self.root, height=10, width=50)
        self.log_text.grid(row=7, column=0, columnspan=2)

        # график
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.chart = FigureCanvasTkAgg(self.figure, self.root)
        self.chart.get_tk_widget().grid(row=0, column=2, rowspan=6)

        # меню
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Меню", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.root.quit)

    def add_entry(self):
        date = self.date_entry.get()
        start = self.start_time_entry.get()
        end = self.end_time_entry.get()
        comment = self.comment_entry.get()

        try:
            entry = SleepEntry(date, start, end, comment)
            self.sleep_entries.append(entry)
            self.tree.insert("", "end",
                             values=(entry.date, entry.start_time, entry.end_time, entry.duration, entry.comment))
            self.log(f"Добавлена запись: {entry.date}, {entry.duration} часов")
            self.update_chart()
        except InvalidInputException as e:
            messagebox.showerror("Ошибка ввода", str(e))
            self.log(f"Ошибка ввода: {e}")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def update_chart(self):
        dates = [entry.date for entry in self.sleep_entries]
        durations = [entry.duration for entry in self.sleep_entries]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(dates, durations, marker='o')
        ax.set_title('Продолжительность сна')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Часы сна')
        self.chart.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = SleepTrackerApp(root)
    root.mainloop()