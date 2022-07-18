from PySide2 import QtWidgets, QtCore
import bpy


class MyWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.setWindowTitle("Sample PySide2 Window")
        self.setWindowFlags(
            QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        self.initUI()
        self.show()

    def initUI(self):

        btn = QtWidgets.QPushButton("Get selections")
        btn.clicked.connect(self.doIt)

        subsurfBtn = QtWidgets.QPushButton("Add Subsurf modifier")
        subsurfBtn.clicked.connect(self.subsurf)

        self.selList = QtWidgets.QListWidget()

        textField = QtWidgets.QTextEdit("Random text")

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(btn)
        mainLayout.addWidget(QtWidgets.QLabel("Selections are : "))
        mainLayout.addWidget(self.selList)
        mainLayout.addWidget(textField)
        mainLayout.addWidget(subsurfBtn)
        self.setLayout(mainLayout)

    def doIt(self):
        sel = [i for i in bpy.context.scene.objects if i.select_get()]

        selStrs = [i.name for i in sel]

        self.selList.clear()
        self.selList.addItems(selStrs)

    def subsurf(self):
        sel = [i for i in bpy.context.scene.objects if i.select_get()]
        for obj in sel:
            obj.modifiers.new("unko", 'SUBSURF')
