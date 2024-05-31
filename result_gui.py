from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
import sys
class ImageWindow(QWidget):
    def __init__(self,graph_drawing, path_chart):
        super().__init__()
        self.initUI(graph_drawing, path_chart)


    def initUI(self,graph_drawing, path_chart):
        layout = QHBoxLayout()

        # Dodawanie pierwszego obrazu
        label1 = QLabel(self)
        pixmap1 = QPixmap(graph_drawing)
        label1.setPixmap(pixmap1)
        layout.addWidget(label1)

        # Dodawanie drugiego obrazu
        label2 = QLabel(self)
        pixmap2 = QPixmap(path_chart)
        label2.setPixmap(pixmap2)
        layout.addWidget(label2)

        self.setLayout(layout)
        self.setWindowTitle("Result")
        self.show()
def resultwindow(graph_drawing, path_chart):
    app = QApplication(sys.argv)
    result = ImageWindow(graph_drawing,path_chart)
    result.show()
    sys.exit(app.exec_())
