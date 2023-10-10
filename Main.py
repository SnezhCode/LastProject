from PyQt5 import QtWidgets

from window.MainWindow import MainWindow

if __name__ == "__main__":  # if name main
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()  # Принятие главного окна в переменную
    window.show()  # Запуск главного окна
    sys.exit(app.exec_())
