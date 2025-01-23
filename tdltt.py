from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QHBoxLayout, QApplication, QLineEdit, 
    QVBoxLayout, QMessageBox
)
from PySide6.QtGui import QPalette, QColor
import sys
from backendwork import TDLDB


class TestTDL(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TDL Tool v.0.0.1")
        self.resize(800, 100)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        # Title setup
        self.title = QLabel("To Do List")
        self.title.setStyleSheet("""
            color: Purple;
            font-family: 'Brush Script MT';
            font-size: 20px;
            font-weight: bold;
        """)

        self.add_task = QLineEdit()
        self.add_task.setPlaceholderText("Add a task...")
        self.add_task.setStyleSheet("""
            QLineEdit {
                font-family: 'Brush Script MT';
                font-size: 16px;
                color: black;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: black;
                font-style: italic;
            }
        """)

        self.add_btn = QPushButton('Add')
        self.add_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Brush Script MT';
                font-size: 16px;
                color: white;  
                background-color: purple;  
                border: none;
                border-radius: 10px;  
                padding: 7px 17px;  
            }
            QPushButton:hover {
                background-color: #800080;
            }
            QPushButton:pressed {
                background-color: #6a006a;
            }
        """)

        self.search_btn = QPushButton('Delete All Tasks')
        self.search_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Brush Script MT';
                font-size: 16px;
                color: white;  
                background-color: purple;  
                border: none;
                border-radius: 10px;  
                padding: 7px 17px;  
            }
            QPushButton:hover {
                background-color: #800080;
            }
            QPushButton:pressed {
                background-color: #6a006a;
            }
        """)
        self.search_btn.setFixedWidth(200)
        self.search_btn.clicked.connect(self.delete_all_tasks)
        self.add_btn.clicked.connect(self.add_task_to_list)

        self.tasks_left = 0
        self.tasks_rem = QLabel(f"You have {self.tasks_left} task(s) to do.")
        self.tasks_rem.setStyleSheet("""
            color: Purple;
            font-family: 'Brush Script MT';
            font-size: 15px;
            font-weight: bold;
        """)

        # Layouts
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title)
        title_layout.addWidget(self.search_btn)

        total_tasks_layout = QVBoxLayout()
        total_tasks_layout.addWidget(self.tasks_rem)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.add_task)
        input_layout.addWidget(self.add_btn)

        self.task_container = QVBoxLayout()  

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(title_layout)
        self.main_layout.addLayout(total_tasks_layout)
        self.main_layout.addLayout(input_layout)
        self.main_layout.addLayout(self.task_container)
        self.setLayout(self.main_layout)

        # Backend
        self.tasks_db = TDLDB()

        self.load_tasks()

    def load_tasks(self):
        tasks = self.tasks_db.all_tasks()  
        self.tasks_left = len(tasks)  
        self.tasks_rem.setText(f"You have {self.tasks_left} task(s) to do.")

        if tasks:
            for task in tasks:
                task_text = task[0]
                task_layout = self.create_task_layout(task_text)
                self.task_container.addLayout(task_layout)

    def add_task_to_list(self):
        self.task_text = self.add_task.text().strip()
        if self.task_text:
            self.tasks_db.add_task(self.task_text)
            self.tasks_left += 1
            self.tasks_rem.setText(f"You have {self.tasks_left} task(s) to do.")
            task_layout = self.create_task_layout(self.task_text)
            self.task_container.addLayout(task_layout)
            self.add_task.clear()
        else:
            self.show_error_message("No task added", "Please add a task and try again.")

    def create_task_layout(self, task_text):
        task_layout = QHBoxLayout()

        task_label = QLabel(task_text)
        task_label.setStyleSheet("""
            color: Black;
            font-family: 'Brush Script MT';
            font-size: 16px;
            font-weight: bold;
        """)

        self.check_btn = QPushButton("OK")
        self.check_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Brush Script MT';
                font-size: 10px;
                color: white;  
                background-color: purple;  
                border: none;
                border-radius: 10px;  
                padding: 7px 17px;  
            }
            QPushButton:hover {
                background-color: #800080;
            }
            QPushButton:pressed {
                background-color: #6a006a;
            }
        """)

        self.del_btn = QPushButton("X")
        self.del_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Brush Script MT';
                font-size: 16px;
                color: white;  
                background-color: purple;  
                border: none;
                border-radius: 10px;  
                padding: 7px 17px;  
            }
            QPushButton:hover {
                background-color: #800080;
            }
            QPushButton:pressed {
                background-color: #6a006a;
            }
        """)

        # Pass the task_text along with task_layout to delete_task
        self.check_btn.clicked.connect(lambda: self.mark_task_done(task_label, self.check_btn))
        self.del_btn.clicked.connect(lambda: self.delete_task(task_layout, task_text))

        task_layout.addWidget(task_label)
        task_layout.addWidget(self.check_btn)
        task_layout.addWidget(self.del_btn)

        return task_layout

    def mark_task_done(self, task_label, check_btn):
        font = task_label.font()
        font.setStrikeOut(True)  
        task_label.setFont(font)  

        if self.tasks_left > 0:
            self.tasks_left -= 1
            self.tasks_rem.setText(f"You have {self.tasks_left} task(s) to do.")

        check_btn.setEnabled(False)  

    def delete_task(self, task_layout, task_text):
        # Delete the task from the database
        self.tasks_db.del_task(task_text)

        # Remove the task layout from the UI
        for i in reversed(range(task_layout.count())):
            widget = task_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.task_container.removeItem(task_layout)

        # Update task count
        if self.tasks_left > 0:
            self.tasks_left -= 1
            self.tasks_rem.setText(f"You have {self.tasks_left} task(s) to do.")

    def delete_all_tasks(self):
        print("Deleting all tasks...")

        self.tasks_db.del_all_tasks()

        # Clear all task widgets from the UI
        for i in reversed(range(self.task_container.count())):
            widget = self.task_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.tasks_left = 0
        self.tasks_rem.setText(f"You have {self.tasks_left} task(s) to do.")

        print("All tasks deleted from database.")

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def closeEvent(self, event):
        print("Closed TDL tool.")
        self.tasks_db.close_db()
        event.accept()


def main():
    app = QApplication(sys.argv)
    tdl = TestTDL()
    tdl.show()
    app.exec()


if __name__ == "__main__":
    main()
