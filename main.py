import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from UI.maingui import Ui_Form


def msgbox_dailog_func(msginfo_lst):
    msg = QMessageBox()
    msg.setIcon(msginfo_lst[0])

    msg.setWindowTitle(msginfo_lst[1])
    msg.setText(msginfo_lst[2])
    msg.setInformativeText(msginfo_lst[3])
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # set some var
        self.tmp_path = ""
        self.mkvmerge_path = "C:\\Program Files\\MKVToolNix\\mkvmerge.exe"

        self.btn_handler_mth()

    def btn_handler_mth(self):
        self.ui.addfile_btn.clicked.connect(self.addfile_mth)
        self.ui.adddir_btn.clicked.connect(self.adddir_mth)

    def addfile_mth(self):
        # TODO: fix why i can't see the (mk Files) option??
        filenames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", self.tmp_path, "mk Files (*.mkv, *.mks, *.mka);; All Files (*)")
        if filenames:
            self.tree_lst_preview_mth(filenames)

    def adddir_mth(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder", self.tmp_path)
        # see if the user select a folder or not
        if folder_name:
            os.chdir(folder_name)
            my_current_dir = os.getcwd()

            # see if the folder is empty or not
            if len(os.listdir(folder_name)) == 0:
                msginfo_lst = [QMessageBox.Warning, "Empty Folder Warning",
                               "The Folder is Empty!!",
                               "No File Or Folder will be added."]
                msgbox_dailog_func(msginfo_lst)

                # if the user cancel the select dialog I have to asign False
                # or the fileNames will be undefined and the program will crash
                # filenames = False
            else:
                # make the name(s) in fileNames list look the same as the format from the getOpenFileNames
                cwdpath = my_current_dir.replace("\\", "/")
                filenames = []
                for f_name in os.listdir(my_current_dir):
                    if QFileInfo(f_name).suffix().lower() == "mkv":
                        filenames.append(f"{cwdpath}/{f_name}")

                self.tree_lst_preview_mth(filenames)
       # else:
            # if the user cancel the select dialog I have to asign False
            # or the fileNames will be undefined and the program will crash
            # filenames = False

    def tree_lst_preview_mth(self, filenames):
        print(filenames)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
