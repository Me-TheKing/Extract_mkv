import sys
import os
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFileInfo, QThread, pyqtSignal
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


class RunMkvmergeThread(QThread):
    """
    Runs a mux thread and output the result in realtime.
    """
    output_changed = pyqtSignal(str)
    signal_filenames = list()
    cmd_sgnl = str()
    finished = pyqtSignal(list)

    mkvmerge_path = "C:\\Program Files\\MKVToolNix\\mkvmerge.exe"

    def run(self):
        for file in self.signal_filenames:
            if self.cmd_sgnl == "mkv info":
                cmd = f'{self.mkvmerge_path} -i "{file}"'

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_changed.emit(output.strip())

        self.finished.emit(self.signal_filenames)


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # set some var
        self.tmp_path = ""
        # self.mkvmerge_path = "C:\\Program Files\\MKVToolNix\\mkvmerge.exe"

        self.btn_handler_mth()

    def btn_handler_mth(self):
        self.ui.addfile_btn.clicked.connect(self.addfile_mth)
        self.ui.adddir_btn.clicked.connect(self.adddir_mth)

    def addfile_mth(self):
        # TODO: add more extintions video
        filenames, _ = QFileDialog.getOpenFileNames(self, "Get File(s)", self.tmp_path, "Video Files (*.mkv *.mp4 *.ts *.avi);; mk Files (*.mkv *mka *.mks)")
        if filenames:
            self.read_file_track_mth(filenames)

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
            else:
                # make the name(s) in fileNames list look the same as the format from the getOpenFileNames
                cwdpath = my_current_dir.replace("\\", "/")
                filenames = []
                for f_name in os.listdir(my_current_dir):
                    if QFileInfo(f_name).suffix().lower() == "mkv":
                        filenames.append(f"{cwdpath}/{f_name}")

                # if filenames is not empty then we call the read_file_track_mth
                if len(filenames):
                    self.read_file_track_mth(filenames)

    def read_file_track_mth(self, filenames):
        self.info_cmd = RunMkvmergeThread()
        self.info_cmd.cmd_sgnl = "mkv info"
        self.info_cmd.signal_filenames = filenames
        self.info_cmd.output_changed.connect(self.on_output_changed_mth)
        self.info_cmd.finished.connect(self.complete_dialog_mth)
        self.info_cmd.start()

    def on_output_changed_mth(self, output):
        print(output)

    def complete_dialog_mth(self, filenames):
        print(filenames)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
