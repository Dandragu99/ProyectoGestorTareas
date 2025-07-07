import sys
from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QListWidget, QHBoxLayout, QDialog, QMessageBox)


USERS_DB = {}

class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de usuario")
        self.setGeometry(300, 300, 300, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Campos de usuario y contraseña
        self.username_label = QLabel("Nuevo usuario:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Nueva contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Botón de registro
        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Guardar usuario en la base de datos
        USERS_DB[username] = password
        QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
        self.accept()


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar sesión")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Nombre de usuario:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Botón para abrir la ventana de registro
        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.open_register_window)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if USERS_DB.get(username) == password:
            self.accept()  # Cierra la ventana y permite acceder al gestor de tareas
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def open_register_window(self):
        register_window = RegisterWindow()
        register_window.exec()


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de tareas")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Añadir nueva tarea")
        self.layout.addWidget(self.task_input)

        self.add_button = QPushButton("Añadir tarea")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        buttons_layout = QHBoxLayout()

        self.delete_button = QPushButton("Eliminar Seleccionada")
        self.delete_button.clicked.connect(self.delete_task)
        buttons_layout.addWidget(self.delete_button)

        self.complete_button = QPushButton("Marcar completada")
        self.complete_button.clicked.connect(self.mark_completed)
        buttons_layout.addWidget(self.complete_button)

        self.layout.addLayout(buttons_layout)
        self.setLayout(self.layout)

    def add_task(self):
        task = self.task_input.text()
        self.task_list.addItem(task)
        self.task_input.clear()

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))

    def mark_completed(self):
        selected_items = self.task_list.selectedItems()
        for item in selected_items:
            if "(Completada)" not in item.text():
                item.setText(item.text() + " (Completada)")


if __name__ == "__main__":
    app = QApplication([])

    login = LoginWindow()
    if login.exec() == QDialog.Accepted:
        window = TaskManager()
        window.show()
        sys.exit(app.exec())
