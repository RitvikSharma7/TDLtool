from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QHBoxLayout, QApplication, QLineEdit, 
    QVBoxLayout, QMessageBox
)
from PySide6.QtGui import QFont, QFontDatabase,QPalette,QColor
import sys


class TestTDL(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDL Tool v.0.0.1")
        self.resize(800, 100)

        # Title setup
        self.title = QLabel("To Do List")
        font_id = QFontDatabase.addApplicationFont("C:\\Users\\conta\\MyPythonProgramming\\TDLproject\\HeaderFont.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family)
        custom_font.setPointSize(16)
        self.title.setFont(custom_font)
        self.title.setStyleSheet("color: Black")

        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("lightblue"))  
        self.setPalette(palette)

       
        self.add_task = QLineEdit()
        self.add_task.setPlaceholderText("Add a task...")
        self.add_btn = QPushButton('Add')
        self.add_btn.clicked.connect(self.add_task_to_list)

        # Layouts
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.add_task)
        input_layout.addWidget(self.add_btn)

        self.task_container = QVBoxLayout()  

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(title_layout)
        self.main_layout.addLayout(input_layout)
        self.main_layout.addLayout(self.task_container)
        self.setLayout(self.main_layout)

    def add_task_to_list(self):
        task_text = self.add_task.text().strip()
        if task_text:
            task_layout = self.create_task_layout(task_text)
            self.task_container.addLayout(task_layout)
            self.add_task.clear()
        else:
            self.show_error_message("No task added", "Please add a task and try again.")

    def create_task_layout(self, task_text):
        task_layout = QHBoxLayout()

        task_label = QLabel(task_text)
        check_btn = QPushButton("OK")
        del_btn = QPushButton("X")

        check_btn.clicked.connect(lambda: self.mark_task_done(task_label))
        del_btn.clicked.connect(lambda: self.delete_task(task_layout))

        task_layout.addWidget(task_label)
        task_layout.addWidget(check_btn)
        task_layout.addWidget(del_btn)

        return task_layout

    def mark_task_done(self, task_label):
        font = task_label.font()
        font.setStrikeOut(True)
        task_label.setFont(font)

    def delete_task(self, task_layout):
        for i in reversed(range(task_layout.count())):
            widget = task_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.task_container.removeItem(task_layout)

    def show_error_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()


def main():
    app = QApplication(sys.argv)
    tdl = TestTDL()
    tdl.show()
    app.exec()


if __name__ == "__main__":
    main()
