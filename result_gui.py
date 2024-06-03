from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from time import sleep
import sys
class ImageWindow(QWidget):
    def __init__(self,graph_drawing, path_chart):
        super().__init__()
        self.initUI(graph_drawing, path_chart)


    def initUI(self,graph_drawing, path_chart):
        layout = QHBoxLayout()

        # Dodawanie pierwszego obrazu
        self.label1 = QLabel()
        self.pixmap1 = QPixmap(graph_drawing)
        self.label1.setPixmap(self.pixmap1)
        layout.addWidget(self.label1)

        # Dodawanie drugiego obrazu
        self.label2 = QLabel()
        self.pixmap2 = QPixmap(path_chart)
        self.label2.setPixmap(self.pixmap2)
        layout.addWidget(self.label2)

        self.setLayout(layout)
        self.setWindowTitle("Result")


def resultwindow(graph_drawing, path_chart):
    # app = QApplication(sys.argv)
    result = ImageWindow(graph_drawing,path_chart)
    icon = QIcon()
    icon.addPixmap(QPixmap("antcolony.png"), QIcon.Selected, QIcon.On)
    result.setWindowIcon(icon)
    return result
    # sys.exit(app.exec_())
