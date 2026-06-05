import tkinter as tk
from tkinter import ttk
import numpy as np
import random
from tkinter import messagebox

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix calculator")
        self.root.configure(bg="#F1F5F9")
        
        self.root.geometry("1100x700")
        try:
            self.root.state("zoomed")
        except Exception:
            pass
            
        self.root.minsize(1024, 650)
        
        self.entries_a = []
        self.entries_b = []
        self.result_widgets = []
        
        self.setup_menu()
        self.setup_ui()
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        matrix_menu = tk.Menu(menubar, tearoff=0)
        matrix_menu.add_command(label="Clear A", command=lambda: self.clear_matrix(True))
        matrix_menu.add_command(label="Clear B", command=lambda: self.clear_matrix(False))
        matrix_menu.add_command(label="Random A", command=lambda: self.fill_matrix_random(True))
        matrix_menu.add_command(label="Random B", command=lambda: self.fill_matrix_random(False))
        menubar.add_cascade(label="Matrix", menu=matrix_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def show_about(self):
        messagebox.showinfo("About", "Matrix calculator\nCreated for Matrix Operations.")
        
    def setup_ui(self):
        header_bar = tk.Frame(self.root, bg="#FFFFFF", height=55, bd=0, highlightthickness=1, highlightbackground="#E2E8F0")
        header_bar.pack(fill="x", side="top")
        header_bar.pack_propagate(False)
        
        title_lbl = tk.Label(header_bar, text="Matrix Calculator", font=("Segoe UI", 14, "bold"), fg="#0F172A", bg="#FFFFFF")
        title_lbl.pack(side="left", padx=20, pady=12)
        
        badge_frame = tk.Frame(header_bar, bg="#EEF2FF", padx=8, pady=3, bd=0)
        badge_frame.pack(side="left", pady=15)
        
        badge_lbl = tk.Label(badge_frame, text="Standard", font=("Segoe UI Semibold", 8), fg="#4F46E5", bg="#EEF2FF")
        badge_lbl.pack()
        
        main_frame = tk.Frame(self.root, bg="#F1F5F9", padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#1E293B", fieldbackground="#FFFFFF", rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#F8FAFC", foreground="#64748B", font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#EEF2FF")], foreground=[("selected", "#4F46E5")])
        style.configure("TCombobox", fieldbackground="#FFFFFF", background="#F1F5F9", foreground="#0F172A", arrowcolor="#64748B")
        
        self.create_matrices_list_card(main_frame, 0, 0)
        self.create_preview_card(main_frame, 1, 0)
        
        self.create_matrix_a_card(main_frame, 0, 1)
        self.create_operations_card(main_frame, 1, 1)
        
        self.create_matrix_b_card(main_frame, 0, 2)
        self.create_result_card(main_frame, 1, 2)
        
        self.update_grid_a()
        self.update_grid_b()
        self.tree.selection_set(self.tree.get_children()[2])
        
    def create_card_frame(self, parent, title, r, c):
        card = tk.Frame(parent, bg="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#E2E8F0", padx=12, pady=10)
        card.grid(row=r, column=c, sticky="nsew", padx=8, pady=8)
        
        title_lbl = tk.Label(card, text=title, font=("Segoe UI", 11, "bold"), fg="#1E293B", bg="#FFFFFF")
        title_lbl.pack(anchor="w", pady=(0, 6))
        
        return card

    def create_matrices_list_card(self, parent, r, c):
        card = self.create_card_frame(parent, "Matrices", r, c)
        
        list_frame = tk.Frame(card, bg="#FFFFFF")
        list_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(list_frame, columns=("Name", "Description"), show="headings", height=5)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.column("Name", width=80, anchor="w")
        self.tree.column("Description", width=160, anchor="w")
        
        self.tree.insert("", "end", values=("Zero", "Zero matrix"))
        self.tree.insert("", "end", values=("One", "Identity matrix"))
        self.tree.insert("", "end", values=("A", "Matrix A"))
        self.tree.insert("", "end", values=("B", "Matrix B"))
        self.tree.insert("", "end", values=("A0", "A0 matrix"))
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_matrix_select)

    def create_preview_card(self, parent, r, c):
        card = self.create_card_frame(parent, "Preview", r, c)
        
        self.preview_name_lbl = tk.Label(card, text="Name: ", font=("Segoe UI", 10), fg="#475569", bg="#FFFFFF")
        self.preview_name_lbl.pack(anchor="w")
        
        self.preview_desc_lbl = tk.Label(card, text="Description: ", font=("Segoe UI", 10), fg="#475569", bg="#FFFFFF")
        self.preview_desc_lbl.pack(anchor="w", pady=(0, 6))
        
        grid_container = tk.Frame(card, bg="#334155", padx=8, pady=8, bd=0, highlightthickness=1, highlightbackground="#1E293B")
        grid_container.pack(fill="both", expand=True, pady=5)
        
        self.preview_grid_frame = tk.Frame(grid_container, bg="#334155")
        self.preview_grid_frame.place(relx=0.5, rely=0.5, anchor="center")

    def create_matrix_a_card(self, parent, r, c):
        card = self.create_card_frame(parent, "Matrix A", r, c)
        
        dim_frame = tk.Frame(card, bg="#FFFFFF")
        dim_frame.pack(fill="x", pady=2)
        
        tk.Label(dim_frame, text="Rows: ", font=("Segoe UI Semibold", 9), fg="#475569", bg="#FFFFFF").pack(side="left")
        self.rows_a_var = tk.StringVar(value="3")
        rows_combo = ttk.Combobox(dim_frame, textvariable=self.rows_a_var, values=["1", "2", "3", "4", "5", "6"], width=3, state="readonly")
        rows_combo.pack(side="left", padx=2)
        rows_combo.bind("<<ComboboxSelected>>", lambda e: self.update_grid_a())
        
        tk.Label(dim_frame, text="Cols: ", font=("Segoe UI Semibold", 9), fg="#475569", bg="#FFFFFF").pack(side="left", padx=(8, 0))
        self.cols_a_var = tk.StringVar(value="3")
        cols_combo = ttk.Combobox(dim_frame, textvariable=self.cols_a_var, values=["1", "2", "3", "4", "5", "6"], width=3, state="readonly")
        cols_combo.pack(side="left", padx=2)
        cols_combo.bind("<<ComboboxSelected>>", lambda e: self.update_grid_a())
        
        grid_container = tk.Frame(card, bg="#334155", padx=8, pady=8, bd=0, highlightthickness=1, highlightbackground="#1E293B")
        grid_container.pack(fill="both", expand=True, pady=5)
        
        self.grid_frame_a = tk.Frame(grid_container, bg="#334155")
        self.grid_frame_a.place(relx=0.5, rely=0.5, anchor="center")
        
        btn_frame = tk.Frame(card, bg="#FFFFFF")
        btn_frame.pack(fill="x", pady=(4, 0))
        
        self.create_util_button(btn_frame, "Clear", lambda: self.clear_matrix(True)).pack(side="left", padx=3, fill="x", expand=True)
        self.create_util_button(btn_frame, "Zeros", lambda: self.fill_matrix_zeros(True)).pack(side="left", padx=3, fill="x", expand=True)
        self.create_util_button(btn_frame, "Random", lambda: self.fill_matrix_random(True)).pack(side="left", padx=3, fill="x", expand=True)

    def create_matrix_b_card(self, parent, r, c):
        card = self.create_card_frame(parent, "Matrix B", r, c)
        
        dim_frame = tk.Frame(card, bg="#FFFFFF")
        dim_frame.pack(fill="x", pady=2)
        
        tk.Label(dim_frame, text="Rows: ", font=("Segoe UI Semibold", 9), fg="#475569", bg="#FFFFFF").pack(side="left")
        self.rows_b_var = tk.StringVar(value="3")
        rows_combo = ttk.Combobox(dim_frame, textvariable=self.rows_b_var, values=["1", "2", "3", "4", "5", "6"], width=3, state="readonly")
        rows_combo.pack(side="left", padx=2)
        rows_combo.bind("<<ComboboxSelected>>", lambda e: self.update_grid_b())
        
        tk.Label(dim_frame, text="Cols: ", font=("Segoe UI Semibold", 9), fg="#475569", bg="#FFFFFF").pack(side="left", padx=(8, 0))
        self.cols_b_var = tk.StringVar(value="3")
        cols_combo = ttk.Combobox(dim_frame, textvariable=self.cols_b_var, values=["1", "2", "3", "4", "5", "6"], width=3, state="readonly")
        cols_combo.pack(side="left", padx=2)
        cols_combo.bind("<<ComboboxSelected>>", lambda e: self.update_grid_b())
        
        grid_container = tk.Frame(card, bg="#334155", padx=8, pady=8, bd=0, highlightthickness=1, highlightbackground="#1E293B")
        grid_container.pack(fill="both", expand=True, pady=5)
        
        self.grid_frame_b = tk.Frame(grid_container, bg="#334155")
        self.grid_frame_b.place(relx=0.5, rely=0.5, anchor="center")
        
        btn_frame = tk.Frame(card, bg="#FFFFFF")
        btn_frame.pack(fill="x", pady=(4, 0))
        
        self.create_util_button(btn_frame, "Clear", lambda: self.clear_matrix(False)).pack(side="left", padx=3, fill="x", expand=True)
        self.create_util_button(btn_frame, "Zeros", lambda: self.fill_matrix_zeros(False)).pack(side="left", padx=3, fill="x", expand=True)
        self.create_util_button(btn_frame, "Random", lambda: self.fill_matrix_random(False)).pack(side="left", padx=3, fill="x", expand=True)

    def create_operations_card(self, parent, r, c):
        card = self.create_card_frame(parent, "Operations", r, c)
        
        output_frame = tk.Frame(card, bg="#FFFFFF")
        output_frame.pack(fill="x", pady=2)
        
        tk.Label(output_frame, text="Output:", font=("Segoe UI Semibold", 10), fg="#0F172A", bg="#FFFFFF").pack(side="left")
        self.output_entry = tk.Entry(output_frame, font=("Segoe UI Semibold", 10), bg="#F8FAFC", fg="#0F172A", bd=0, highlightthickness=1, highlightbackground="#E2E8F0", highlightcolor="#4F46E5")
        self.output_entry.pack(side="left", padx=8, fill="x", expand=True, ipady=4)
        
        btn_grid = tk.Frame(card, bg="#FFFFFF")
        btn_grid.pack(fill="both", expand=True, pady=(5, 0))
        
        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)
        btn_grid.columnconfigure(2, weight=1)
        
        self.create_op_button(btn_grid, "A + B", lambda: self.run_op("add"), 0, 0, "#4F46E5", "#FFFFFF", "#3730A3")
        self.create_op_button(btn_grid, "A - B", lambda: self.run_op("sub"), 0, 1, "#4F46E5", "#FFFFFF", "#3730A3")
        self.create_op_button(btn_grid, "A * B", lambda: self.run_op("mul"), 0, 2, "#4F46E5", "#FFFFFF", "#3730A3")
        
        self.create_op_button(btn_grid, "A + x", lambda: self.run_op("add_x"), 1, 0, "#F1F5F9", "#0F172A", "#E2E8F0")
        self.create_op_button(btn_grid, "A - x", lambda: self.run_op("sub_x"), 1, 1, "#F1F5F9", "#0F172A", "#E2E8F0")
        self.create_op_button(btn_grid, "A * x", lambda: self.run_op("mul_x"), 1, 2, "#F1F5F9", "#0F172A", "#E2E8F0")
        
        self.create_op_button(btn_grid, "A ^ -1", lambda: self.run_op("inv"), 2, 0, "#F8FAFC", "#334155", "#E2E8F0")
        self.create_op_button(btn_grid, "A ^ x", lambda: self.run_op("pow_x"), 2, 1, "#F8FAFC", "#334155", "#E2E8F0")
        self.create_op_button(btn_grid, "Transp(A)", lambda: self.run_op("trans"), 2, 2, "#F8FAFC", "#334155", "#E2E8F0")
        
        self.create_op_button(btn_grid, "Trace(A)", lambda: self.run_op("trace"), 3, 0, "#F8FAFC", "#334155", "#E2E8F0")
        self.create_op_button(btn_grid, "Rank(A)", lambda: self.run_op("rank"), 3, 1, "#F8FAFC", "#334155", "#E2E8F0")
        self.create_op_button(btn_grid, "Det(A)", lambda: self.run_op("det"), 3, 2, "#F8FAFC", "#334155", "#E2E8F0")
        
        self.create_op_button(btn_grid, "Min(A)", lambda: self.run_op("min"), 4, 0, "#F8FAFC", "#334155", "#E2E8F0")
        self.create_op_button(btn_grid, "Max(A)", lambda: self.run_op("max"), 4, 1, "#F8FAFC", "#334155", "#E2E8F0")
        self.create_op_button(btn_grid, "Reset", self.reset_all, 4, 2, "#FFF1F2", "#DF1C1C", "#FFE4E6")

    def create_result_card(self, parent, r, c):
        card = self.create_card_frame(parent, "Result", r, c)
        
        grid_container = tk.Frame(card, bg="#334155", padx=8, pady=8, bd=0, highlightthickness=1, highlightbackground="#1E293B")
        grid_container.pack(fill="both", expand=True, pady=5)
        
        self.result_grid_frame = tk.Frame(grid_container, bg="#334155")
        self.result_grid_frame.place(relx=0.5, rely=0.5, anchor="center")

    def create_util_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg="#F8FAFC",
            fg="#475569",
            activebackground="#E2E8F0",
            activeforeground="#0F172A",
            relief="solid",
            bd=1,
            highlightthickness=0,
            font=("Segoe UI Semibold", 9),
            cursor="hand2"
        )
        
        def on_enter(e):
            btn.config(bg="#E2E8F0", fg="#0F172A")
        def on_leave(e):
            btn.config(bg="#F8FAFC", fg="#475569")
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_op_button(self, parent, text, command, r, c, bg_color, fg_color, hover_color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            activebackground=hover_color,
            activeforeground=fg_color,
            relief="solid",
            bd=1,
            highlightthickness=0,
            font=("Segoe UI Semibold", 9),
            height=1,
            pady=5,
            cursor="hand2"
        )
        btn.grid(row=r, column=c, padx=3, pady=3, sticky="ew")
        
        def on_enter(e):
            btn.config(bg=hover_color)
        def on_leave(e):
            btn.config(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_styled_entry(self, parent):
        entry = tk.Entry(
            parent,
            width=6,
            font=("Segoe UI Semibold", 10),
            justify="center",
            bd=0,
            bg="#F8FAFC",
            fg="#0F172A",
            highlightthickness=1,
            highlightbackground="#E2E8F0",
            highlightcolor="#4F46E5"
        )
        def on_focus_in(e):
            entry.config(bg="#FFFFFF")
        def on_focus_out(e):
            entry.config(bg="#F8FAFC")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return entry

    def update_grid_a(self):
        for row in self.entries_a:
            for entry in row:
                entry.destroy()
        self.entries_a.clear()
        
        rows = int(self.rows_a_var.get())
        cols = int(self.cols_a_var.get())
        
        initial_values = [
            [1, 5, 4],
            [2, 1, 1],
            [1, 1, 123]
        ]
        
        for r in range(rows):
            row_entries = []
            for c in range(cols):
                entry = self.create_styled_entry(self.grid_frame_a)
                entry.grid(row=r, column=c, padx=3, pady=3, ipady=4)
                
                if r < len(initial_values) and c < len(initial_values[0]) and rows == 3 and cols == 3:
                    entry.insert(0, str(initial_values[r][c]))
                else:
                    entry.insert(0, "0")
                    
                row_entries.append(entry)
            self.entries_a.append(row_entries)
            
        self.sync_tree_preview()

    def update_grid_b(self):
        for row in self.entries_b:
            for entry in row:
                entry.destroy()
        self.entries_b.clear()
        
        rows = int(self.rows_b_var.get())
        cols = int(self.cols_b_var.get())
        
        initial_values = [
            [2, 5, 0],
            [3, 4, 0],
            [2, 0, 0]
        ]
        
        for r in range(rows):
            row_entries = []
            for c in range(cols):
                entry = self.create_styled_entry(self.grid_frame_b)
                entry.grid(row=r, column=c, padx=3, pady=3, ipady=4)
                
                if r < len(initial_values) and c < len(initial_values[0]) and rows == 3 and cols == 3:
                    entry.insert(0, str(initial_values[r][c]))
                else:
                    entry.insert(0, "0")
                    
                row_entries.append(entry)
            self.entries_b.append(row_entries)
            
        self.sync_tree_preview()

    def clear_matrix(self, is_matrix_a):
        entries = self.entries_a if is_matrix_a else self.entries_b
        for row in entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.sync_tree_preview()

    def fill_matrix_zeros(self, is_matrix_a):
        entries = self.entries_a if is_matrix_a else self.entries_b
        for row in entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
        self.sync_tree_preview()

    def fill_matrix_random(self, is_matrix_a):
        entries = self.entries_a if is_matrix_a else self.entries_b
        for row in entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(0, str(random.randint(-9, 9)))
        self.sync_tree_preview()

    def get_matrix_data(self, entries):
        rows = len(entries)
        cols = len(entries[0])
        matrix = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                val_str = entries[r][c].get().strip()
                if not val_str:
                    raise ValueError("Fill all matrix cells.")
                try:
                    matrix[r, c] = float(val_str)
                except ValueError:
                    raise ValueError(f"Bad number: '{val_str}'")
        return matrix

    def get_scalar_x(self):
        val_str = self.output_entry.get().strip()
        if not val_str:
            raise ValueError("Enter scalar x in Output field.")
        try:
            return float(val_str)
        except ValueError:
            raise ValueError(f"Bad scalar: '{val_str}'")

    def run_op(self, op):
        try:
            matrix_a = self.get_matrix_data(self.entries_a)
            
            if op == "add":
                matrix_b = self.get_matrix_data(self.entries_b)
                if matrix_a.shape != matrix_b.shape:
                    raise ValueError("Dimensions must match.")
                self.display_result_matrix(matrix_a + matrix_b)
                
            elif op == "sub":
                matrix_b = self.get_matrix_data(self.entries_b)
                if matrix_a.shape != matrix_b.shape:
                    raise ValueError("Dimensions must match.")
                self.display_result_matrix(matrix_a - matrix_b)
                
            elif op == "mul":
                matrix_b = self.get_matrix_data(self.entries_b)
                if matrix_a.shape[1] != matrix_b.shape[0]:
                    raise ValueError("Inner dimensions must match.")
                self.display_result_matrix(np.dot(matrix_a, matrix_b))
                
            elif op == "add_x":
                x = self.get_scalar_x()
                self.display_result_matrix(matrix_a + x)
                
            elif op == "sub_x":
                x = self.get_scalar_x()
                self.display_result_matrix(matrix_a - x)
                
            elif op == "mul_x":
                x = self.get_scalar_x()
                self.display_result_matrix(matrix_a * x)
                
            elif op == "inv":
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    raise ValueError("Matrix must be square.")
                self.display_result_matrix(np.linalg.inv(matrix_a))
                
            elif op == "pow_x":
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    raise ValueError("Matrix must be square.")
                x = int(self.get_scalar_x())
                self.display_result_matrix(np.linalg.matrix_power(matrix_a, x))
                
            elif op == "trans":
                self.display_result_matrix(matrix_a.T)
                
            elif op == "trace":
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    raise ValueError("Matrix must be square.")
                self.display_scalar_result(np.trace(matrix_a))
                
            elif op == "rank":
                self.display_scalar_result(np.linalg.matrix_rank(matrix_a))
                
            elif op == "det":
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    raise ValueError("Matrix must be square.")
                self.display_scalar_result(np.linalg.det(matrix_a))
                
            elif op == "min":
                self.display_scalar_result(np.min(matrix_a))
                
            elif op == "max":
                self.display_scalar_result(np.max(matrix_a))
                
        except ValueError as ex:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, str(ex))
        except Exception as ex:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, f"Error: {str(ex)}")

    def format_val(self, val):
        if np.isclose(val, round(val)):
            return str(int(round(val)))
        formatted = f"{val:.4f}"
        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")
        return formatted

    def clear_result(self):
        for widget in self.result_widgets:
            if isinstance(widget, list):
                for w in widget:
                    w.destroy()
            else:
                widget.destroy()
        self.result_widgets.clear()

    def display_result_matrix(self, matrix):
        self.clear_result()
        rows, cols = matrix.shape
        for r in range(rows):
            row_widgets = []
            for c in range(cols):
                val = matrix[r, c]
                disp_str = self.format_val(val)
                
                entry = tk.Entry(
                    self.result_grid_frame,
                    width=6,
                    font=("Segoe UI Semibold", 10),
                    justify="center",
                    bd=0,
                    bg="#F8FAFC",
                    fg="#0F172A",
                    highlightthickness=1,
                    highlightbackground="#E2E8F0",
                    highlightcolor="#4F46E5"
                )
                entry.insert(0, disp_str)
                entry.config(state="readonly")
                entry.grid(row=r, column=c, padx=3, pady=3, ipady=4)
                row_widgets.append(entry)
            self.result_widgets.append(row_widgets)

    def display_scalar_result(self, val):
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.format_val(val))
        self.clear_result()

    def on_matrix_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        name, desc = item["values"]
        self.preview_name_lbl.config(text=f"Name: {name}")
        self.preview_desc_lbl.config(text=f"Description: {desc}")
        self.update_preview_grid(name)

    def sync_tree_preview(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        name = item["values"][0]
        self.update_preview_grid(name)

    def update_preview_grid(self, name):
        for widget in self.preview_grid_frame.winfo_children():
            widget.destroy()
            
        if name == "Zero":
            data = np.zeros((3, 3))
        elif name == "One":
            data = np.eye(3)
        elif name == "A":
            try:
                data = self.get_matrix_data(self.entries_a)
            except Exception:
                data = np.zeros((3, 3))
        elif name == "B":
            try:
                data = self.get_matrix_data(self.entries_b)
            except Exception:
                data = np.zeros((3, 3))
        elif name == "A0":
            data = np.array([[1, 5, 4], [2, 1, 1], [1, 1, 123]])
        else:
            data = np.zeros((3, 3))
            
        rows, cols = data.shape
        for r in range(rows):
            for c in range(cols):
                val = data[r, c]
                disp = self.format_val(val)
                lbl = tk.Label(
                    self.preview_grid_frame,
                    text=disp,
                    width=6,
                    font=("Segoe UI Semibold", 10),
                    bg="#F8FAFC",
                    fg="#0F172A",
                    bd=0,
                    highlightthickness=1,
                    highlightbackground="#E2E8F0"
                )
                lbl.grid(row=r, column=c, padx=3, pady=3, ipady=4)

    def reset_all(self):
        self.output_entry.delete(0, tk.END)
        self.clear_result()
        self.rows_a_var.set("3")
        self.cols_a_var.set("3")
        self.rows_b_var.set("3")
        self.cols_b_var.set("3")
        self.update_grid_a()
        self.update_grid_b()

root = tk.Tk()
app = MatrixCalculator(root)
root.mainloop()
