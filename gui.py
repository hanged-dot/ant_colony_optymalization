from main import main

from PyQt5 import QtWidgets,QtCore
import sys
import os
import json


from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QRadioButton, QGroupBox, QCheckBox, QStyleFactory, QApplication, QVBoxLayout, QPushButton, \
    QLineEdit, QGridLayout, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPixmap


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
        button.clicked.connect(self.click)
        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(buttonLabel)
        topLayout.addWidget(button)
        topLayout.addStretch(1)
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
        self.topLeftGroupBox = QGroupBox("Chosen configuration")
        self.graphQComboBox1 = QComboBox()
        populate_combo_box(self.graphQComboBox1,"./graphs")
        self.configQComboBox = QComboBox()
        populate_combo_box(self.configQComboBox,"./configs")
        self.configQComboBox.currentIndexChanged.connect(self.updateTopRightGroupBox)
        layout = QVBoxLayout()
        layout.addWidget(self.graphQComboBox1)
        layout.addWidget(self.configQComboBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Chosen configuration")
        config= self.configQComboBox.currentText()
        with open(f"configs/{config}", 'r') as f:
            data = json.load(f)
        self.ants_info= QLabel("Ant number: " + str(data["ants"]))
        self.days_info=QLabel("Days number: " + str(data["days"]))
        self.pheromones_info=QLabel("Pheromones deposited by ants: " + str(data["pheromones"]))
        self.evaporation_info =QLabel("Pheromones evraporation rate: " + str(data["evaporation"]))
        self.importance_of_pheromones_info = QLabel("Importance of pheromones: " + str(data["importance_of_pheromones"]))
        self.importance_of_distance_info = QLabel("Importance of distance: " + str(data["importance_of_distance"]))
        layout = QVBoxLayout()
        layout.addWidget(self.ants_info)
        layout.addWidget(self.days_info)
        layout.addWidget(self.pheromones_info)
        layout.addWidget(self.evaporation_info)
        layout.addWidget(self.importance_of_pheromones_info)
        layout.addWidget(self.importance_of_distance_info)

        layout.addStretch(5)
        self.topRightGroupBox.setLayout(layout)
    def updateTopRightGroupBox(self,index):
        config = self.configQComboBox.itemText(index)
        with open(f"configs/{config}", 'r') as f:
            data = json.load(f)
        self.ants_info.setText("Ant number: " + str(data["ants"]))
        self.days_info.setText("Days number: " + str(data["days"]))
        self.pheromones_info.setText("Pheromones deposited by ants: " + str(data["pheromones"]))
        self.evaporation_info.setText("Pheromones evraporation rate: " + str(data["evaporation"]))
        self.importance_of_pheromones_info.setText("Importance of pheromones: " + str(data["importance_of_pheromones"]))
        self.importance_of_distance_info.setText("Importance of distance: " + str(data["importance_of_distance"]))


    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Choose your own configuration")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(False)



        self.ants = QLineEdit()
        ants_label = QLabel("Ant number:")
        ants_label.setBuddy(self.ants)
        self.days = QLineEdit()
        days_label =QLabel("Days number:")
        days_label.setBuddy(self.days)
        self.pheromones = QLineEdit()
        pheromones_label = QLabel("Pheromones:")
        pheromones_label.setBuddy(self.pheromones)
        self.evaporation = QLineEdit()
        evaporation_label = QLabel("Evaporation:")
        evaporation_label.setBuddy(self.evaporation)
        self.importance_of_pheromones = QLineEdit()
        importance_of_pheromones_label = QLabel("Importance of_pheromones:")
        importance_of_pheromones_label.setBuddy(self.importance_of_pheromones)
        self.importance_of_distance = QLineEdit()
        importance_of_distance_label = QLabel("Importance of_distance:")
        importance_of_distance_label.setBuddy(self.importance_of_distance)
        graphchoice = QLabel("Choose graph variant: ")
        self.graphQComboBox2 = QComboBox()
        populate_combo_box(self.graphQComboBox2, "./graphs")


        layout = QGridLayout()
        layout.addWidget(ants_label, 0, 0, 1, 2)
        layout.addWidget(self.ants,0,2,1,2)
        layout.addWidget(days_label, 1, 0, 1, 2)
        layout.addWidget(self.days,1,2,1,2)
        layout.addWidget(pheromones_label, 2, 0, 1, 2)
        layout.addWidget(self.pheromones,2,2,1,2)
        layout.addWidget(evaporation_label, 3, 0, 1, 2)
        layout.addWidget(self.evaporation,3,2,1,2)
        layout.addWidget(importance_of_pheromones_label, 4, 0, 1, 2)
        layout.addWidget(self.importance_of_pheromones,4,2,1,2)
        layout.addWidget(importance_of_distance_label, 5, 0, 1, 2)
        layout.addWidget(self.importance_of_distance,5,2,1,2)
        layout.addWidget(graphchoice,6,0,1,2)
        layout.addWidget(self.graphQComboBox2,6,2,1,2)

        layout.setRowStretch(6, 2)
        self.bottomRightGroupBox.setLayout(layout)

    def click(self):
        # Collect data from widgets
        if self.bottomRightGroupBox.isChecked():
            config_data = {
                'ants': int(self.ants.text()),
                'days': int(self.days.text()),
                'pheromones': float(self.pheromones.text()),
                'evaporation': float(self.evaporation.text()),
                'importance_of_pheromones': float(self.importance_of_pheromones.text()),
                'importance_of_distance': float(self.importance_of_distance.text()),
            }
            graphfilename = self.graphQComboBox2.currentText()
            config_folder = './configs'
            config_files = [f for f in os.listdir(config_folder) if f.startswith('config_') and f.endswith('.json')]
            if config_files:
                max_num = max([int(f.split('_')[1].split('.')[0]) for f in config_files])
                next_num = max_num + 1
            else:
                next_num = 1

            config_filename = f'config_{next_num}.json'
            config_filepath = os.path.join(config_folder, config_filename)

            # Save data to the new JSON file
            with open(config_filepath, 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
            print(f"Configuration saved as {config_filename}!")
            self.result_window = main(graphfilename, config_filename)
            self.result_window.show()
        else:
            graphfilename = self.graphQComboBox1.currentText()
            configfilename = self.configQComboBox.currentText()
            self.result_window = main(graphfilename, configfilename)
            self.result_window.show()

def populate_combo_box(box, directory):
    try:
        # Get the list of files in the directory
        files = os.listdir(directory)
        # Add each file to the combo box
        for file in files:
            box.addItem(file)
    except Exception as e:
        print(f"Error reading directory: {e}")

def window():
    app=QtWidgets.QApplication(sys.argv)
    win=MyWindow()
    icon = QIcon()
    icon.addPixmap(QPixmap("antcolony.png"), QIcon.Selected, QIcon.On)
    win.setWindowIcon(icon)
    win.show()
    sys.exit(app.exec_())
window()




