from PyQt5 import QtWidgets,QtCore
import sys

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QRadioButton, QGroupBox, QCheckBox, QStyleFactory, QApplication, QVBoxLayout, QPushButton, \
    QLineEdit, QSpinBox, QDateTimeEdit, QSlider, QScrollBar, QDial, QGridLayout, QLabel
from PyQt5.QtGui import QIcon


class MyWindow(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(MyWindow,self).__init__(parent)
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()


        buttonLabel = QtWidgets.QLabel('Hi! Choose your simulation variant and start simulation:')
        button = QPushButton(self)
        button.setText("Start Simulation")
        buttonLabel.setBuddy(button)
        button.clicked.connect(click)
        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(buttonLabel)
        topLayout.addWidget(button)
        topLayout.addStretch(1)

        # todo implement checking group 1 or 3 between your own config of given
        self.bottomRightGroupBox.toggled.connect(self.topRightGroupBox.setDisabled)
        self.bottomRightGroupBox.toggled.connect(self.topLeftGroupBox.setDisabled)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 0,1,2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        self.setWindowTitle("Ant Colony Optimization")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowIcon(QIcon('./antcolony.png'))
        self.setLayout(mainLayout)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Config 1")
        radioButton2 = QRadioButton("Config 2")
        #radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)


        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Chosen configuration")
        #todo implement showing confing uppon choosing from group 1
        layout = QVBoxLayout()
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)



    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Choose your own configuration")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(False)

        ants = QLineEdit()
        ants_label = QLabel("Ant number:")
        ants_label.setBuddy(ants)
        days = QLineEdit()
        days_label =QLabel("Days number:")
        days_label.setBuddy(days)
        pheromones = QLineEdit()
        pheromones_label = QLabel("Pheromones:")
        pheromones_label.setBuddy(pheromones)
        evaporation = QLineEdit()
        evaporation_label = QLabel("Evaporation:")
        evaporation_label.setBuddy(evaporation)
        importance_of_pheromones = QLineEdit()
        importance_of_pheromones_label = QLabel("Importance of_pheromones:")
        importance_of_pheromones_label.setBuddy(importance_of_pheromones)
        importance_of_distance = QLineEdit()
        importance_of_distance_label = QLabel("Importance of_distance:")
        importance_of_distance_label.setBuddy(importance_of_distance)


        layout = QGridLayout()
        layout.addWidget(ants_label, 0, 0, 1, 2)
        layout.addWidget(ants,0,2,1,2)
        layout.addWidget(days_label, 1, 0, 1, 2)
        layout.addWidget(days,1,2,1,2)
        layout.addWidget(pheromones_label, 2, 0, 1, 2)
        layout.addWidget(pheromones,2,2,1,2)
        layout.addWidget(evaporation_label, 3, 0, 1, 2)
        layout.addWidget(evaporation,3,2,1,2)
        layout.addWidget(importance_of_pheromones_label, 4, 0, 1, 2)
        layout.addWidget(importance_of_pheromones,4,2,1,2)
        layout.addWidget(importance_of_distance_label, 5, 0, 1, 2)
        layout.addWidget(importance_of_distance,5,2,1,2)

        layout.setRowStretch(5, 2)
        self.bottomRightGroupBox.setLayout(layout)



def window():
    app=QtWidgets.QApplication(sys.argv)
    win=MyWindow()
    win.show()
    sys.exit(app.exec_())
def click(self):
    print('Clicked')
window()