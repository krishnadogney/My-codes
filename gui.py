from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 672)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QGroupBox(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(40, 70, 721, 531))
        self.title.setObjectName(" Sample title ")

        self.comboBox = QtWidgets.QComboBox(self.title)
        self.comboBox.setGeometry(QtCore.QRect(90, 60, 211, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["Select","Node","Group","Node to Group"])
        self.comboBox.currentIndexChanged.connect(self.selectionchange)

        self.label = QtWidgets.QLabel(self.title)
        self.label.setGeometry(QtCore.QRect(20, 80, 68, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.title)
        self.label_2.setGeometry(QtCore.QRect(20, 200, 68, 19))
        self.label_2.setObjectName("label_2")

        self.comboBox_2 = QtWidgets.QComboBox(self.title)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 180, 211, 41))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(["Select","Node", "Group","Node from Group"])
        self.comboBox_2.currentIndexChanged.connect(self.selectionchange)

        self.textEdit = QtWidgets.QTextEdit(self.title)
        self.textEdit.setGeometry(QtCore.QRect(390, 60, 107, 41))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setDisabled(True)
        self.textEdit_2 = QtWidgets.QTextEdit(self.title)
        self.textEdit_2.setGeometry(QtCore.QRect(580, 60, 107, 41))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setDisabled(True)
        self.label_3 = QtWidgets.QLabel(self.title)
        self.label_3.setGeometry(QtCore.QRect(417, 20, 51, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.title)
        self.label_4.setGeometry(QtCore.QRect(610, 20, 68, 19))
        self.label_4.setObjectName("label_4")
        self.textEdit_3 = QtWidgets.QTextEdit(self.title)
        self.textEdit_3.setGeometry(QtCore.QRect(390, 180, 107, 41))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.title)
        self.textEdit_4.setGeometry(QtCore.QRect(580, 180, 107, 41))
        self.textEdit_4.setObjectName("textEdit_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setTitle(_translate("MainWindow", "Title"))
        self.label.setText(_translate("MainWindow", "Add"))
        self.label_2.setText(_translate("MainWindow", "Delete"))
        self.label_3.setText(_translate("MainWindow", "Node"))
        self.label_4.setText(_translate("MainWindow", "Group"))

    def selectionchange(self, i):

        if self.comboBox.currentText() == "Select":
            # print(self.comboBox.itemText(i))
            self.textEdit.setDisabled(True)
            self.textEdit_2.setDisabled(True)

        if self.comboBox.currentText()=="Node":
            print(self.comboBox.itemText(i))
            self.textEdit.setDisabled(False)
            self.textEdit_2.setDisabled(True)
        if self.comboBox.currentText() == "Group":
                print(self.comboBox.itemText(i))
                self.textEdit.setDisabled(True)
                self.textEdit_2.setDisabled(False)

        if self.comboBox.currentText() == "Node to Group":
                    print(self.comboBox.itemText(i))
                    self.textEdit.setDisabled(False)
                    self.textEdit_2.setDisabled(False)

        # for count in range(self.comboBox.count()):
        #     print(self.comboBox.itemText(count))
        #
        # print ("Current index", i, "selection changed ", self.comboBox.currentText())





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

