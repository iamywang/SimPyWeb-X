import sys

from PyQt5.QtWidgets import QApplication

from main import BrowserWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = BrowserWindow()
    MainWindow.show()
    sys.exit(app.exec_())
