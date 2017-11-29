import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import *
working_node = 0
node_config = {"cmd": 0 ,"no_node":0,"port_no": 0,"X_location": 0,"Y_location": 0,"group":0}
class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(50,50,800,500)
        self.setWindowTitle("Emulator")
        self.setWindowIcon(QtGui.QIcon('ISO-HR-290X230-comp-based-job-roles.png'))
        #self.node_config = {}

        extrctAction1 = QtGui.QAction("Quit", self)
        extrctAction1.setShortcut("Ctrl+Q")
        extrctAction1.setStatusTip('Leav the App')
        extrctAction1.triggered.connect(self.close_application)

        extrctAction2 = QtGui.QAction("New", self)
        extrctAction2.setShortcut("Ctrl+N")
        extrctAction2.setStatusTip('make new system')
        extrctAction2.triggered.connect(self.close_application)

        extrctAction3 = QtGui.QAction("Save", self)
        extrctAction3.setShortcut("Ctrl+S")
        extrctAction3.setStatusTip('Save system')
        extrctAction3.triggered.connect(self.close_application)

        extrctAction4 = QtGui.QAction("Add Node", self)
        extrctAction4.setStatusTip('Add a new node to system')
        extrctAction4.triggered.connect(self.close_application)

        extrctAction5 = QtGui.QAction("Remove node", self)
        extrctAction5.setStatusTip('Remove node from system system')
        extrctAction5.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()

        # for file menu
        fileMenu1 = mainMenu.addMenu('&File')
        fileMenu1.addAction(extrctAction2)
        fileMenu1.addAction(extrctAction3)
        fileMenu1.addAction(extrctAction1)

        # for edit menu
        fileMenu2 = mainMenu.addMenu('&Edit')
        fileMenu2.addAction(extrctAction4)
        fileMenu2.addAction(extrctAction5)

        # for run menu
        fileMenu3 = mainMenu.addMenu('&Run')

        # for help meun
        fileMenu4 = mainMenu.addMenu('&Help')

        self.home()

    def home(self):
        l1 = QtGui.QLabel("Welcome to Wireless Sensor Emulator",self)
        l1.resize(l1.sizeHint())
        l1.setAlignment(Qt.AlignCenter)
        l1.move(250,50)

        extractAction = QtGui.QAction(QtGui.QIcon("run_button.png"), "click to run emulator", self)
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)

        extractAction = QtGui.QAction(QtGui.QIcon("pause.png"), "click to pause", self)
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)

        extractAction = QtGui.QAction(QtGui.QIcon("Button-Add-icon.png"), "click to add nodes", self)
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)

        extractAction = QtGui.QAction(QtGui.QIcon("Button-Delete-icon.png"), "click to remove node", self)
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)

        self.add_node_buttons()



    def add_node_buttons(self):

        btn7 = QtGui.QPushButton("command", self)
        btn7.resize(btn7.sizeHint())
        btn7.move(50, 100)
        btn7.clicked.connect(self.getitem1)
        self.box7 = QLineEdit(self)
        self.box7.move(200, 100)
        l7 = QtGui.QLabel("Select ", self)
        l7.resize(410, 30)
        l7.move(330, 90)
        l7 = QtGui.QLabel("*Required field for Adding and Removing Node", self)
        l7.resize(350, 30)
        l7.move(330, 105)

        btn1 = QtGui.QPushButton("Enter no of node", self)
        btn1.resize(btn1.sizeHint())
        # btn1.setStatusTip('Number of nodes you want to add')
        btn1.move(50, 150)
        btn1.clicked.connect(self.getint)
        self.box1 = QLineEdit(self)
        self.box1.move(200, 150)
        self.l1 = QtGui.QLabel("Number of nodes you want to Add or Remove", self)
        self.l1.resize(300, 30)
        self.l1.move(330, 135)
        self.l1 = QtGui.QLabel("*Required field for Adding and Removing Node", self)
        self.l1.resize(270, 30)
        self.l1.move(330, 150)

        btn2 = QtGui.QPushButton("Enter starting port no", self)
        btn2.resize(btn2.sizeHint())
        btn2.move(50, 200)
        btn2.clicked.connect(self.getint1)
        self.box2 = QLineEdit(self)
        self.box2.move(200, 200)
        l2 = QtGui.QLabel("Give the starting port number of the node you want to Add and Remove", self)
        l2.resize(410, 30)
        l2.move(330, 190)
        l2 = QtGui.QLabel("*Required field for Adding and Removing Node", self)
        l2.resize(350, 30)
        l2.move(330, 205)

        btn3 = QtGui.QPushButton("Enter the X location", self)
        btn3.resize(btn3.sizeHint())
        btn3.move(50, 250)
        btn3.clicked.connect(self.getint2)
        self.box3 = QLineEdit(self)
        self.box3.move(200, 250)
        l3 = QtGui.QLabel("Enter the X location of the new node", self)
        l3.resize(350, 30)
        l3.move(330, 240)
        l3 = QtGui.QLabel("Not Required field in case of Removing node", self)
        l3.resize(350, 30)
        l3.move(330, 255)

        btn4 = QtGui.QPushButton("Enter the Y location", self)
        btn4.resize(btn3.sizeHint())
        btn4.move(50, 300)
        btn4.clicked.connect(self.getint3)
        self.box4 = QLineEdit(self)
        self.box4.move(200, 300)
        l4 = QtGui.QLabel("Enter the Y location of the new node", self)
        l4.resize(350, 30)
        l4.move(330, 290)
        l4 = QtGui.QLabel("Not Required field in case of Removing node", self)
        l4.resize(350, 30)
        l4.move(330, 305)

        btn5 = QtGui.QPushButton("Node ordering", self)
        btn5.resize(btn3.sizeHint())
        btn5.move(50, 350)
        btn5.clicked.connect(self.getitem)
        self.box5 = QLineEdit(self)
        self.box5.move(200, 350)
        l5 = QtGui.QLabel("Method to add or remove node", self)
        l5.resize(300, 30)
        l5.move(330, 340)
        l5 = QtGui.QLabel("*Required for both Adding and Removing node", self)
        l5.resize(200, 30)
        l5.move(330, 355)
        l5 = QtGui.QLabel("Sequential - Adding node sequentially. Specify the starting port number  ", self)
        l5.resize(500, 30)
        l5.move(330, 370)
        l5 = QtGui.QLabel("and XY location.", self)
        l5.resize(200, 30)
        l5.move(330, 385)
        l5 = QtGui.QLabel("Manually - specify all the port numbers and location seperated by comma.  ", self)
        l5.resize(500, 30)
        l5.move(330, 400)
        # print(self.node_config)

        btn6 = QtGui.QPushButton("Enter", self)
        btn6.resize(btn6.sizeHint())
        btn6.move(200, 400)
        btn6.clicked.connect(self.getlist)
        btn6.clicked.connect(self.Total_working_node)
        self.show()

    def Total_working_node(self,working_node):
        global node_config
        if node_config["cmd"] == "Add node":
            working_node =  working_node +int(node_config["no_node"])
        if node_config["cmd"] == "Remove node":
            working_node = working_node + int(node_config["no_node"])
            print(working_node)
        return working_node

    def getlist(self):
        print(node_config)
        return node_config

    def close_application(self):
        print("I think this is done")
        sys.exit()

    def getint(self):
        no_node, ok = QInputDialog.getText(self, "No of nodes", "Enter the nomber of node")
        print("Number of node is:", no_node)
        if ok:
            self.box1.setText(str(no_node))
        node_config["no_node"] = no_node
        return no_node

    def getint1(self):
        port_no, ok = QInputDialog.getText(self, "Port number", "Enter a port number")
        print("port number is:", port_no)
        if ok:
            self.box2.setText(str(port_no))
        node_config["port_no"] = port_no
        return port_no

    def getint2(self):
        X_loc, ok = QInputDialog.getText(self, "X_location", "Enter X Location")
        print("X Location of starting port is:", X_loc)
        if ok:
            self.box3.setText(str(X_loc))
        node_config["X_location"] = X_loc
        return X_loc

    def getint3(self):
        Y_loc, ok = QInputDialog.getText(self, "Y_location", "Enter Y Location")
        print("Y Location of starting port is:", Y_loc)
        if ok:
            self.box4.setText(str(Y_loc))
        node_config["Y_Location"] = Y_loc
        return Y_loc


    def getitem(self):
        items = ("Sequencial","Manual")

        group, ok = QInputDialog.getItem(self, "Preference",
                                        "NOde ordering Preference", items, 0, False)
        print("group is: ", group)
        if ok and group:
            self.box5.setText(group)
        node_config["group"] = group
        return group

    def getitem1(self):
        items1 = ("Add node","Remove node")

        cmd, ok1 = QInputDialog.getItem(self, "Command",
                                        "Add/Remove node", items1, 0, False)
        print("group is: ", cmd)
        if ok1 and cmd:
            self.box7.setText(cmd)
        node_config["cmd"] = cmd
        return cmd

    def close_application(self):
        print("I think this is done")
        sys.exit()






if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    print(working_node)
    app.exec_()
