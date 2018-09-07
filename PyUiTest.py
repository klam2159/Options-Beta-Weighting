from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])
dlg = uic.loadUi("QtDesignertest.ui")

dlg.show()
app.exec()

