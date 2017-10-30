#This is a GUI program for Emulator
#The first widget is to small pop-up window with 3 buttons
#first button = creat new system
#Second button = add node in the existing system
#third button = remove node from the current system
#The user will have to click the first button to creat new system
#on clicking the first button 5  pop up input box will appear one after other
#the first input is the number of node the user want to creat in the system
#the second pop up input box will ask for the starting port number
#the third pop up input box will ask for user about the sequential entry of a node or user defin node
#the forth and fifth box rill ask the location of the node in the system namey X and Y cordinate
#The second button in the system is for adding node in the system
#If the user click on this button the same 5 input popup bow will appear one after other
# with the same input as in the button 1
#The Third button is for removing node
#It will show 3 input popup menu
#the first one will ask for how many node you want to remove
#the second will ask for the starting sequence number
#the third will ask for squenential or not.



import sys
from PyQt5.QtWidgets import QApplication, QWidget,QToolTip, QPushButton
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        #self.setToolTip('This is a <b>QWidget</b> widget')
        btn1 = QPushButton('Make new system', self)
        btn1.setToolTip('Push this button for creating new system')


        btn2 = QPushButton('add node', self)
        btn2.setToolTip('Push this button for adding new node')


        btn3 = QPushButton('remove node', self)
        btn3.setToolTip('Push this button for deleting node')

        btn1.resize(btn1.sizeHint())
        btn1.move(50, 50)

        btn2.resize(btn2.sizeHint())
        btn2.move(50, 100)

        btn3.resize(btn3.sizeHint())
        btn3.move(50, 150)


        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))


        btn1.clicked.connect(self.on_click1)
        btn2.clicked.connect(self.on_click2)
        btn3.clicked.connect(self.on_click3)


        self.show()
    @pyqtSlot()
    def on_click1(self):
        i, okPressed = QInputDialog.getInt(self, "Enter_Number_of_node", "Integer:", 0, 0, 1000000, 1)
        j, okPressed = QInputDialog.getInt(self, "Starting_Port_Number", "Integer:", 40002, 0, 1000000, 1)
        sequence, okPressed = QInputDialog.getText(self, "Preference for Sequence Number", "-seq for Sequential numbering:", QLineEdit.Normal, "")
        if sequence != "seq":
            for p in i:
                X[p], okPressed = QInputDialog.getInt(self, "X_location of the node", "Integer:", 0, 0, 1000000, 1)
                Y[p], okPressed = QInputDialog.getInt(self, "X_location of the node", "Integer:", 0, 0, 1000000, 1)
        if okPressed:
            print(i, j)

    @pyqtSlot()
    def on_click2(self):

        add_i, okPressed = QInputDialog.getInt(self, "Enter_Number_of_node_you_want _add", "Integer:", 0, 0, 1000000, 1)
        add_j, okPressed = QInputDialog.getInt(self, "Starting_Port_Number", "Integer:", 40002, 0, 1000000, 1)
        add_sequence, okPressed = QInputDialog.getText(self, "Preference for Sequence Number",
                                                   "-seq for Sequential numbering:", QLineEdit.Normal, "")
        if add_sequence != "seq":
            for p in i:
                add_X[p], okPressed = QInputDialog.getInt(self, "X_location of the node", "Integer:", 0, 0, 1000000, 1)
                add_Y[p], okPressed = QInputDialog.getInt(self, "X_location of the node", "Integer:", 0, 0, 1000000, 1)
        if okPressed:
            print(add_i, add_j)

    @pyqtSlot()
    def on_click3(self):

        remove_i, okPressed = QInputDialog.getInt(self, "Enter_Number_of_node_you_want _remove", "Integer:", 0, 0, 1000000, 1)
        remove_j, okPressed = QInputDialog.getInt(self, "Starting_Port_Number", "Integer:", 40002, 0, 1000000, 1)
        remove_sequence, okPressed = QInputDialog.getText(self, "Preference for Sequence Number",
                                                       "-seq for Sequential numbering:", QLineEdit.Normal, "")

        if okPressed:
            print(remove_i, remove_j)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())