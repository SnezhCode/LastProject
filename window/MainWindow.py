from PyQt5 import QtWidgets

from DataBase import cursor, conn
from window.BoneWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):  # Класс главного окна
    def __init__(self):
        super(MainWindow, self).__init__()  # Инициализация главного окна и скелета сгенерированного окна
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Установка видимости кнопок
        self.ui.pushButton.setVisible(False)
        self.ui.pushButton_3.setVisible(False)
        self.ui.pushButton_6.setVisible(False)

        # Обновление "treeWidget"
        self.update_treeWidget()

        # Срабатывает когда пользователь нажимает на строку "treeWidget"
        self.ui.treeWidget.itemClicked.connect(self.item_click)

        # Установка функций к кнопкам
        self.ui.pushButton.clicked.connect(self.edit_employee)
        self.ui.pushButton_2.clicked.connect(lambda: self.update_treeWidget(True))
        self.ui.pushButton_3.clicked.connect(self.delete_employee)
        self.ui.pushButton_4.clicked.connect(self.update_treeWidget)
        self.ui.pushButton_5.clicked.connect(self.add_employee)
        self.ui.pushButton_6.clicked.connect(self.remove_selection)

    # Функция при нажатии на строку "treeWidget"
    def item_click(self):
        self.clearLines()  # Функция отчистки полей ввода

        # Установка видимости кнопок
        self.ui.pushButton_4.setVisible(False)
        self.ui.pushButton_5.setVisible(False)
        self.ui.pushButton_6.setVisible(True)
        self.ui.pushButton_3.setVisible(True)
        self.ui.pushButton.setVisible(True)

    # Функция обновления "treeWidget" чтобы не писать подобную при поиске ФИО задан параметр при определенной кнопке
    # который равен True
    def update_treeWidget(self, param=False):
        # Отчистка "treeWidget" для последующего заполнения
        self.ui.treeWidget.clear()
        # Получаем данные из базы данных

        # Если сработала кнопка с ФИО
        if param:
            if self.ui.pushButton_2.text() != 'Сбросить':
                # Поиск по заданному имени
                cursor.execute("SELECT * FROM employees WHERE name=?", (self.ui.lineEdit.text(),))
                data = cursor.fetchall()
                self.ui.pushButton_2.setText('Сбросить')  # Изменения текста на кнопке
            else:
                # Поиск по всей базе данных
                cursor.execute("SELECT * FROM employees")
                data = cursor.fetchall()
                self.ui.pushButton_2.setText('Поиск по ФИО')  # Изменения текста на кнопке
        else:
            # Поиск по всей базе данных
            cursor.execute("SELECT * FROM employees")
            data = cursor.fetchall()

        # Заполняем "treeWidget" данными из базы данных
        for row in data:
            item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            item.setText(0, str(row[0]))  # ID
            item.setText(1, row[1])  # ФИО
            item.setText(2, row[2])  # Телефон
            item.setText(3, row[3])  # Email
            item.setText(4, str(row[4]))  # Зарплата

    # Функция для снятия выделения в "treeWidget"
    def remove_selection(self):
        self.ui.pushButton.setText('Изменить')  # Изменения текста на кнопке
        self.clearLines()  # Функция отчистки полей ввода
        self.ui.treeWidget.setCurrentItem(None)  # Снятие выделения в "treeWidget"

        # Установка видимости кнопок
        self.ui.pushButton_6.setVisible(False)
        self.ui.pushButton_3.setVisible(False)
        self.ui.pushButton.setVisible(False)
        self.ui.pushButton_4.setVisible(True)
        self.ui.pushButton_5.setVisible(True)

    # Функция для добавления сотрудника
    def add_employee(self):
        # Получение данных из полей ввода
        name = self.ui.lineEdit.text()
        phone = self.ui.lineEdit_2.text()
        email = self.ui.lineEdit_3.text()
        salary = self.ui.doubleSpinBox.value()

        # Сохранение в базу данных
        cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
                       (name, phone, email, salary))
        conn.commit()

        self.clearLines()  # Функция отчистки полей ввода
        self.update_treeWidget()  # Обновление "treeWidget"

    # Функция для удаления сотрудника
    def delete_employee(self):
        # Получение выделенной строки "treeWidget"
        selected_item = self.ui.treeWidget.currentItem()
        # Получение данных выделенной строки "treeWidget"
        values = [selected_item.text(column) for column in range(self.ui.treeWidget.columnCount())]

        # Удаление из базы данных
        cursor.execute("DELETE FROM employees WHERE id=?", (values[0],))
        conn.commit()

        self.remove_selection()  # Функция снятия выделения
        self.update_treeWidget()  # Обновление "treeWidget"

    # Функция для редактирования сотрудника
    def edit_employee(self):
        # Получение выделенной строки "treeWidget"
        selected_item = self.ui.treeWidget.currentItem()
        # Получение данных выделенной строки "treeWidget"
        values = [selected_item.text(column) for column in range(self.ui.treeWidget.columnCount())]

        # Если текст на кнопке равен
        if self.ui.pushButton.text() == "Изменить":
            # Установка текста в поля для ввода
            self.ui.lineEdit.setText(values[1])
            self.ui.lineEdit_2.setText(values[2])
            self.ui.lineEdit_3.setText(values[3])
            self.ui.doubleSpinBox.setValue(float(values[4]))

            # Установка текста для кнопки
            self.ui.pushButton.setText('Подтвердить')

        elif self.ui.pushButton.text() == "Подтвердить":
            # Обновление данных в базе данных
            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?",
                           (self.ui.lineEdit.text(), self.ui.lineEdit.text(), self.ui.lineEdit.text(),
                            self.ui.doubleSpinBox.value(), values[0]))
            conn.commit()

            self.clearLines()  # Функция отчистки полей ввода
            self.ui.pushButton.setText('Изменить')  # Установка текста для кнопки
            self.update_treeWidget()  # Обновление "treeWidget"

    # Функция отчистки полей ввода
    def clearLines(self):
        # Отчистка полей ввода
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.doubleSpinBox.clear()
