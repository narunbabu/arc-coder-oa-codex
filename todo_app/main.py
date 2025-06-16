import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import platform
from datetime import datetime

from .db_manager import DBManager


class TodoApp(tk.Tk):
    """Main application window."""

    GEOM_FILE = Path(".todo_geometry")

    def __init__(self, db_path: str = "tasks_notes.db"):
        super().__init__()
        self.title("To-Do & Notes Manager")
        self.minsize(800, 600)
        self.db = DBManager(db_path)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._create_widgets()
        self.bind("<Unmap>", self._on_minimize)
        self.bind("<Map>", self._on_restore)
        self.bubble = None
        if self.GEOM_FILE.exists():
            self.geometry(self.GEOM_FILE.read_text())

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.tasks_frame = ttk.Frame(self.notebook)
        self.notes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tasks_frame, text="To-Do")
        self.notebook.add(self.notes_frame, text="Notes")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self._init_tasks_tab()
        self._init_notes_tab()

    # --- Tasks Tab ---
    def _init_tasks_tab(self):
        top = ttk.Frame(self.tasks_frame)
        top.pack(fill=tk.X)
        add_btn = ttk.Button(top, text="Add", command=self.add_task_dialog)
        del_btn = ttk.Button(top, text="Delete", command=self.delete_task)
        done_btn = ttk.Button(top, text="Mark Done", command=self.mark_done)
        add_btn.pack(side=tk.LEFT, padx=2, pady=2)
        del_btn.pack(side=tk.LEFT, padx=2, pady=2)
        done_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.task_tree = ttk.Treeview(
            self.tasks_frame,
            columns=("title", "due", "priority", "status"),
            show="headings",
        )
        for col in ("title", "due", "priority", "status"):
            self.task_tree.heading(col, text=col.title())
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_tasks()

    def refresh_tasks(self):
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)
        for row in self.db.list_tasks():
            self.task_tree.insert(
                "",
                tk.END,
                iid=row[0],
                values=(row[1], row[2] or "", row[3], row[4]),
            )

    def add_task_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("New Task")
        ttk.Label(dlg, text="Title").grid(row=0, column=0)
        title_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=title_var).grid(row=0, column=1)
        ttk.Label(dlg, text="Due Date (YYYY-MM-DD)").grid(row=1, column=0)
        due_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=due_var).grid(row=1, column=1)
        ttk.Label(dlg, text="Priority").grid(row=2, column=0)
        prio_var = tk.IntVar(value=0)
        ttk.Entry(dlg, textvariable=prio_var).grid(row=2, column=1)
        ttk.Button(
            dlg,
            text="Add",
            command=lambda: self._add_task_from_dialog(dlg, title_var, due_var, prio_var),
        ).grid(row=3, column=0, columnspan=2)

    def _add_task_from_dialog(self, dlg, title_var, due_var, prio_var):
        title = title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "Title required")
            return
        due = due_var.get().strip() or None
        self.db.add_task(title, due, prio_var.get())
        dlg.destroy()
        self.refresh_tasks()
        self._update_bubble()

    def delete_task(self):
        sel = self.task_tree.selection()
        if not sel:
            return
        task_id = int(sel[0])
        self.db.delete_task(task_id)
        self.refresh_tasks()
        self._update_bubble()

    def mark_done(self):
        sel = self.task_tree.selection()
        if not sel:
            return
        task_id = int(sel[0])
        self.db.update_task(task_id, status="done")
        self.refresh_tasks()
        self._update_bubble()

    # --- Notes Tab ---
    def _init_notes_tab(self):
        left = ttk.Frame(self.notes_frame)
        left.pack(side=tk.LEFT, fill=tk.Y)
        right = ttk.Frame(self.notes_frame)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notes_list = tk.Listbox(left)
        self.notes_list.pack(fill=tk.Y, expand=True)
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Add", command=self.add_note_dialog).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Delete", command=self.delete_note).pack(side=tk.LEFT)
        self.notes_list.bind("<<ListboxSelect>>", lambda e: self.show_note())

        self.note_text = tk.Text(right, wrap="word")
        self.note_text.pack(fill=tk.BOTH, expand=True)
        self.refresh_notes()

    def refresh_notes(self):
        self.notes_list.delete(0, tk.END)
        for row in self.db.list_notes():
            self.notes_list.insert(tk.END, f"{row[0]}: {row[1]}")

    def add_note_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("New Note")
        ttk.Label(dlg, text="Title").grid(row=0, column=0)
        title_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=title_var).grid(row=0, column=1)
        ttk.Button(
            dlg,
            text="Add",
            command=lambda: self._add_note_from_dialog(dlg, title_var),
        ).grid(row=1, column=0, columnspan=2)

    def _add_note_from_dialog(self, dlg, title_var):
        title = title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "Title required")
            return
        self.db.add_note(title, "")
        dlg.destroy()
        self.refresh_notes()

    def show_note(self):
        sel = self.notes_list.curselection()
        if not sel:
            return
        idx = int(self.notes_list.get(sel[0]).split(":", 1)[0])
        note = next((n for n in self.db.list_notes() if n[0] == idx), None)
        if note:
            self.note_text.delete("1.0", tk.END)
            self.note_text.insert("1.0", note[2])

    def delete_note(self):
        sel = self.notes_list.curselection()
        if not sel:
            return
        idx = int(self.notes_list.get(sel[0]).split(":", 1)[0])
        self.db.delete_note(idx)
        self.note_text.delete("1.0", tk.END)
        self.refresh_notes()

    # --- Bubble overlay ---
    def _on_minimize(self, event):
        if self.state() == "iconic" and platform.system() == "Windows":
            self.show_bubble()

    def _on_restore(self, event):
        if self.bubble:
            self.bubble.destroy()
            self.bubble = None

    def show_bubble(self):
        if self.bubble:
            return
        self.bubble = tk.Toplevel(self)
        self.bubble.overrideredirect(True)
        self.bubble.attributes("-topmost", True)
        frame = ttk.Frame(self.bubble, padding=10)
        frame.pack()
        self.bubble_label = ttk.Label(frame, text="")
        self.bubble_label.pack(side=tk.LEFT)
        ttk.Button(frame, text="+", command=self.add_task_dialog).pack(side=tk.LEFT)
        self._update_bubble()
        self.bubble.update_idletasks()
        w = self.bubble.winfo_width()
        h = self.bubble.winfo_height()
        sw = self.winfo_screenwidth()
        self.bubble.geometry(f"{w}x{h}+{sw - w - 10}+100")
        self.bubble.bind("<Button-1>", lambda e: self._restore_from_bubble())

    def _restore_from_bubble(self):
        self.deiconify()
        if self.bubble:
            self.bubble.destroy()
            self.bubble = None

    def _update_bubble(self):
        if not self.bubble:
            return
        pending = sum(1 for t in self.db.list_tasks() if t[4] != "done")
        self.bubble_label.config(text=f"Pending: {pending}")

    def on_close(self):
        self.GEOM_FILE.write_text(self.geometry())
        self.db.close()
        self.destroy()


def main():
    app = TodoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
