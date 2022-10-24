# This Python file uses the following encoding: utf-8

## Sight Reading Choicer By Propp
## Version 0.0.1

## Have you got a stupidly big collection of sheet music and
## want to sight read it randomly? This program is for you!
## It chooses a random (pdf) file and keeps track of it. Then
## you can decide whether you wanna rank it (noteworthy, difficult)
## so you can have another look at it in the future.
## A file that's already been chosen will not be chosen again.
## This way, you will eventually sight read your whole collection
## (and remember which pieces were too difficult/noteworthy,
## so you can compare with your past self).

## Warning!
## This program is written very poorly. I wrote it ages ago when
## I was just getting started programming. You will find every
## possible bad coding practice here.
## Also the reasoning behind it is either very stupid or nonexistent.
## At the time I was only concerned in getting the thing to work...

## That said, I thought to publish it anyway, just in case anybody
## needs a little program like this to devour random sheet music.

import sys
import os, random
from PyQt5.QtWidgets import *
from pathlib import Path
from PyQt5 import *
import sightreadingchoicer
import SSRC_Settings
from SSRC_Settings import Ui_Dialog
import subprocess
from configparser import ConfigParser
import json
from os.path import exists
from collections import Counter
import shutil
from distutils.dir_util import copy_tree

def debug():
    print("debug")

# Initialising configuration
#if not config.has_section('already picked files'):
#    config.add_section('already picked files')
#    file_number = 0
#    config.set('already picked files', str(file_number), 'ignore')

file_path = ""
file_extension = "pdf"

subdir = "config_files"
# create subfolder if it doesn't exist
Path(subdir).mkdir(parents=True, exist_ok=True)
# obtain current directory
here = os.path.dirname(os.path.realpath(__file__))
# this is the list from which the files are picked
picker_list_filename = os.path.join(here, subdir, "pickerList.json")
# this contains all files, it gets updated
all_list_filename = os.path.join(here, subdir, "allList.json")
# this list contains a list of already chosen files
already_chosen_filename = os.path.join(here, subdir, "alreadyChosen.json")
# this list is useful when new files are added
added_list_filename = os.path.join(here, subdir, "addedList.json")
# this list contains all the pieces marked as difficult
difficult_list_filename = os.path.join(here, subdir, "difficultPieces.json")
# this list contains all the pieces marked as noteworthy
noteworthy_list_filename = os.path.join(here, subdir, "noteworthyPieces.json")
# this file contains informations such as the chosen directory
configuration_filename = os.path.join(here, subdir, "config.ini")
isFirstTime = False
# the next two variables are totally useless, could be removed
directoryHasNoFiles = ""
directoryNotChosenYet = ""
difficultPiecesAreOver = ""
noteworthyPiecesAreOver = ""
config = ConfigParser()
# this could probably be put inside of a function, buuuut...
all_list = []
added_list = []
picker_list = []
already_chosen_list = []
difficult_list = []
noteworthy_list = []
current_difficult_piece = 0
current_noteworthy_piece = 0
def generate_config_files(list_filename, list):
    # open output file for writing
    with open(list_filename, 'w') as filehandle:
        json.dump(list, filehandle)

def initialize_configuration():
    global all_list, added_list, noteworthy_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, config, difficult_list, current_noteworthy_piece, current_difficult_piece
    if not config.has_section("directory_info"):
        if not exists(picker_list_filename):
            all_list = []
            added_list = []
            picker_list = []
            already_chosen_list = []
            difficult_list = []
            noteworthy_list = []
            current_difficult_piece = 0
            current_noteworthy_piece = 0
            # saving directory information
            config.read(configuration_filename)
            print("generating directory info section")
            config.add_section('directory_info')
            # initialising config
            config.set("directory_info", "directoryHasNoFiles", "")
            config.set("directory_info", "currentDir", "")
            config.set("directory_info", "directoryNotChosenYet", "")
            config.set("directory_info", "difficultPiecesAreOver", "")
            config.set("directory_info", "noteworthyPiecesAreOver", "")
            config.set("directory_info", "currentDifficultPiece", str(current_difficult_piece))
            config.set("directory_info", "currentNoteworthyPiece", str(current_noteworthy_piece))


initialize_configuration()


if exists(picker_list_filename):
    # Importing configuration, if it exists
    with open(already_chosen_filename, 'r') as filehandle:
        already_chosen_list = json.load(filehandle)
    with open(picker_list_filename, 'r') as filehandle:
        picker_list = json.load(filehandle)
    print("it exists")

def save_configuration():
    global difficultPiecesAreOver, noteworthyPiecesAreOver, file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, difficult_list, difficult_list_filename, noteworthy_list, noteworthy_list_filename, config, directoryNotChosenYet, directoryHasNoFiles, current_noteworthy_piece, current_difficult_piece
    generate_config_files(all_list_filename, all_list)
    generate_config_files(picker_list_filename, picker_list)
    generate_config_files(already_chosen_filename, already_chosen_list)
    generate_config_files(difficult_list_filename, difficult_list)
    generate_config_files(noteworthy_list_filename, noteworthy_list)
    #generate_config_files(added_list_filename, added_list)
    config.read(configuration_filename)
    config.set("directory_info", "directoryHasNoFiles", directoryHasNoFiles)
    config.set("directory_info", "currentDir", file_path)
    config.set("directory_info", "directoryNotChosenYet", directoryNotChosenYet)
    config.set("directory_info", "currentDifficultPiece", str(current_difficult_piece))
    config.set("directory_info", "currentNoteworthyPiece", str(current_noteworthy_piece))
    config.set("directory_info", "directoryNotChosenYet", "")
    config.set("directory_info", "difficultPiecesAreOver", str(difficultPiecesAreOver))
    config.set("directory_info", "noteworthyPiecesAreOver", str(noteworthyPiecesAreOver))
    with open(configuration_filename, 'w') as f:
        config.write(f)
    config.read(configuration_filename)

def read_configuration():
    global difficultPiecesAreOver, noteworthyPiecesAreOver, file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, difficult_list, difficult_list_filename, noteworthy_list, noteworthy_list_filename, config, directoryNotChosenYet, directoryHasNoFiles, current_noteworthy_piece, current_difficult_piece
    config.read(configuration_filename)
    print("reading configuration... the configuration has the section: ", str(config.has_section("directory_info")))
    if config.has_section("directory_info") and exists(picker_list_filename):
        file_path = config.get("directory_info", "currentDir")
        print("in the function, file path is:", file_path)
        directoryHasNoFiles = config.get("directory_info", "directoryHasNoFiles")
        print("saved file path is:", file_path)
        current_difficult_piece = int(config.get("directory_info", "currentDifficultPiece"))
        print("current difficult piece is:", current_difficult_piece)
        current_noteworthy_piece = int(config.get("directory_info", "currentNoteworthyPiece"))
        print("current noteworthy piece is:", current_noteworthy_piece)
        difficultPiecesAreOver = str(config.get("directory_info", "difficultPiecesAreOver"))
        noteworthyPiecesAreOver = str(config.get("directory_info", "noteworthyPiecesAreOver"))
        with open(already_chosen_filename, 'r') as filehandle:
            already_chosen_list = json.load(filehandle)
        with open(picker_list_filename, 'r') as filehandle:
            picker_list = json.load(filehandle)
        with open(all_list_filename, 'r') as filehandle:
            all_list = json.load(filehandle)
        #with open(added_list_filename, 'r') as filehandle:
            #added_list = json.load(filehandle)
        with open(difficult_list_filename, 'r') as filehandle:
             difficult_list = json.load(filehandle)
        with open(noteworthy_list_filename, 'r') as filehandle:
             noteworthy_list = json.load(filehandle)
        added_list = []

def reset():
    global difficultPiecesAreOver, noteworthyPiecesAreOver, file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, difficult_list, difficult_list_filename, noteworthy_list, noteworthy_list_filename, config, directoryNotChosenYet, directoryHasNoFiles, current_noteworthy_piece, current_difficult_piece
    all_list = []
    added_list = []
    picker_list = []
    difficult_list = []
    noteworthy_list = []
    already_chosen_list = []
    current_difficult_piece = 0
    current_noteworthy_piece = 0
    save_configuration()
    difficultPiecesAreOver = ""
    noteworthyPiecesAreOver = ""


def parse_pdf_files():
    filecount = 0
    global file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, config, directoryNotChosenYet, directoryHasNoFiles, current_noteworthy_piece, current_difficult_piece
    # updating config
    config.read(configuration_filename)
    directoryHasNoFiles = config.get("directory_info", "directoryHasNoFiles")
    # this function generates a list with all pdf files (all_list)
    # inheriting global variables
    global picker_list, all_list, already_chosen_list, added_list
    all_list = []
    # creating a list with all pdf files in a directory
    for root, dirs, files in os.walk(file_path):
        for file in files:
            filecount += 1
            print("found a file")
            if file.endswith(".pdf"):
                temp = os.path.join(root, file)
                if temp not in all_list:
                    if temp not in already_chosen_list:
                        all_list.append(os.path.join(root, file))
                        directoryHasNoFiles = "False"
            else:
                if len(all_list) == 0 and directoryHasNoFiles == "False":
                    # well, the directory is not actually empty, there just aren't pdf files...
                    directoryHasNoFiles = "True"
                    save_configuration()
    if filecount == 0 and exists(picker_list_filename):
        print("there are no files here")
        directoryHasNoFiles = "True"
        save_configuration()
    print("generated list: ", all_list)


    # initially, the two lists are the same, but as soon as a random
    # piece is chosen, the picker list must update itself by removing it



# if __name__ == '__main__':
extension = sys.argv[1] if len(sys.argv) > 1 else file_extension


class SettingsDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        #self.ui = Ui_Dialog()
        self.setupUi(self)
        # in case the file_path exists (from a previous config), write it to
        # the textBrowser.
        global difficultPiecesAreOver, file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, config, directoryNotChosenYet, directoryHasNoFiles
        read_configuration()
        print("in the settingsSS, file path is:", file_path)
        self.selectedDirectoryTextBrowser.setText(file_path)
        self.chooseDirectoryButton.clicked.connect(self.choose_directory)
        self.resetButton.clicked.connect(self.reset_config)
        self.backupButton.clicked.connect(self.backup_config)
        self.restoreButton.clicked.connect(self.restore_config)

    def restore_config(self):
        global subdir
        restore_dir = str(QFileDialog.getExistingDirectory(self, "Select Restore Directory"))
        if not restore_dir == "":
            copy_tree(restore_dir, subdir)
            self.selectedDirectoryTextBrowser.setText(f'successfully restored from directory: "{restore_dir}"')
        else:
            self.selectedDirectoryTextBrowser.setText("didn't restore: directory not chosen")
    def backup_config(self):
        global subdir
        if exists(subdir):
            backup_dir = str(QFileDialog.getExistingDirectory(self, "Select Backup Directory"))
            if not backup_dir == "":
                print(Path(backup_dir))
                copy_tree(subdir, backup_dir)
                # shutil.copytree(subdir, backup_dir)
                self.selectedDirectoryTextBrowser.setText(f'successfully backed up in directory: "{backup_dir}"')
            else:
                self.selectedDirectoryTextBrowser.setText("didn't backup: directory not chosen")
        else:
            self.selectedDirectoryTextBrowser.setText("There is nothing to back-up!")

    def error_window(self, text, win_title, info):
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setInformativeText(info)
        msg.setWindowTitle(win_title)
        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

    def button_clicked(self):
        print("click")

    def choose_directory(self):
        read_configuration()
        msg = QMessageBox.warning(self, 'Choose Directory', 'This action resets configuration, proceed?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) # , QMessageBox.No is the default button
        if msg == QMessageBox.Yes:
            global file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, config, directoryNotChosenYet, directoryHasNoFiles
            print("importing config")
            file_path = str(QFileDialog.getExistingDirectory(self, "Select Directory Where Files Will be Picked From"))
            self.selectedDirectoryTextBrowser.setText(file_path)
            if not file_path == "":
                directoryNotChosenYet = "False"
                directoryHasNoFiles = "False"
            # memorize selected directory to file
            save_configuration()
            # obviously, when a new directory is chosen, the configuration
            # is reset. But what about when the directory changes, but the
            # files are the same (e.g. same folder across different clients)?!
            reset()
            parse_pdf_files()
            picker_list = all_list
            save_configuration()
        else:
            print("ignore")

    def reset_config(self):
        msg = QMessageBox.warning(self, 'Reset Configuration', 'This action resets configuration, proceed?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No) # , QMessageBox.No is the default button
        if msg == QMessageBox.Yes:
            global file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, config, directoryNotChosenYet, directoryHasNoFiles
            # this should be executed when resetting configuration
            # (ask for a confirmation dialog first)
            reset()
            parse_pdf_files()
            picker_list = all_list
            save_configuration()
        else:
           print("ignore")

class SightReadingChoicer(QtWidgets.QMainWindow, sightreadingchoicer.Ui_MainWindow):
    def __init__(self, parent=None):
        super(SightReadingChoicer, self).__init__(parent)
        self.setupUi(self)

        self.newChoiceButton.clicked.connect(debug)
        self.newChoiceButton.clicked.connect(self.cliccato)
        self.newChoiceButton.clicked.connect(self.get_random_files2)
        self.noteworthyButton.clicked.connect(self.noteworthy_piece)
        self.actionPreferences.triggered.connect(self.preferences)
        self.actionPreferences.triggered.connect(self.show_new_window)
        self.difficultButton.clicked.connect(self.difficult_piece)
        #self.chooseDifficultPieceCheckBox.stateChanged.connect(self.clickBox)
        self.updateFilesCheckBox.stateChanged.connect(self.willUpdateFiles)
        self.difficultPieceRadioButton.toggled.connect(self.willChooseDifficultPiece)
        self.randomNewPieceRadioButton.toggled.connect(self.willChooseRandomNewPiece)
        self.noteworthyPieceRadioButton.toggled.connect(self.willChooseNoteworthyPiece)
        self.recheckFiles = False
        # preventing undeclared variables
        self.noteworthyPieceRadioButton.setChecked(True)
        self.difficultPieceRadioButton.setChecked(True)
        self.randomNewPieceRadioButton.setChecked(True)
        # pass
        # self.random_choice = None
    def willUpdateFiles(self, state):
        if state == QtCore.Qt.Checked:
            self.recheckFiles = True
            print('will Update Files')
        else:
            self.recheckFiles = False
            print('will not Update Files')

    def willChooseRandomNewPiece(self):
        if self.randomNewPieceRadioButton.isChecked():
            self.isRandomNewPiece = True
            print("will chose a random piece")
        else:
            self.isRandomNewPiece = False
            print("won't choose a random piece")

    def willChooseDifficultPiece(self):
        if self.difficultPieceRadioButton.isChecked():
            self.isDifficultPiece = True
            print("will chose a difficult piece")
        else:
            self.isDifficultPiece = False
            print("won't choose a difficult piece")

    def willChooseNoteworthyPiece(self):
        if self.noteworthyPieceRadioButton.isChecked():
            self.isNoteworthyPiece = True
            print("will chose a noteworthy piece")
        else:
            self.isNoteworthyPiece = False
            print("won't choose a noteworthy piece")


    def noteworthy_piece(self):
        global noteworthy_list, noteworthyPiecesAreOver, noteworthyPiecesAreOver
        try:
            print("noteworthy")
            print(self.random_choice)
            if self.random_choice not in noteworthy_list:
                noteworthy_list.append(self.random_choice)
                self.textBrowser.setText(f'The piece "{os.path.splitext(os.path.basename(self.random_choice))[0]}" has been marked as noteworthy!')
                noteworthyPiecesAreOver = "False"
            save_configuration()
        except AttributeError:
            self.textBrowser.setText("a piece has not been selected yet")


    def difficult_piece(self):
        global difficult_list, difficultPiecesAreOver, noteworthyPiecesAreOver
        try:
            print("Difficult")
            print(self.random_choice)
            if self.random_choice not in difficult_list:
                difficult_list.append(self.random_choice)
                self.textBrowser.setText(f'The piece "{os.path.splitext(os.path.basename(self.random_choice))[0]}" has been marked as difficult!')
                difficultPiecesAreOver = "False"
            save_configuration()
        except AttributeError:
            self.textBrowser.setText("a piece has not been selected yet")

    def preferences(self):
        self.myDialog = SettingsDialog()
        self.myDialog.show()

    def show_new_window(self, checked):
        if self.myDialog is None:
            self.myDialog = SettingsDialog()
        self.myDialog.show()

# A history function would be great to implement, here, one day.
    def get_random_files2(self, top=file_path):
        global difficultPiecesAreOver, noteworthyPiecesAreOver, file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, difficult_list, difficult_list_filename, noteworthy_list, noteworthy_list_filename, config, directoryNotChosenYet, directoryHasNoFiles, current_noteworthy_piece, current_difficult_piece
        if self.recheckFiles:
            self.update_files()
        # making a random choice
        read_configuration()
        if self.isNoteworthyPiece:
            print("piece is noteworthy")
            if not len(difficult_list) == 0:
                print("choosing noteworthy piece")
                # warning: this is not a real random choice, it is actually a
                # selection of the noteworthy pieces in a cronological order.
                try:
                     self.random_choice = noteworthy_list[current_noteworthy_piece]
                     noteworthyPiecesAreOver = "False"
                     current_noteworthy_piece += 1
                except IndexError:
                    print("the noteworthy pieces are over!!")
                    noteworthyPiecesAreOver = "True"
                    self.textBrowser.setText("noteworthy pieces are over!")

                if not noteworthyPiecesAreOver == "True":
                    # Actual opening of the file: this should be put outside of the if
                    # and should be present only once in the function, but...
                    self.textBrowser.setText(f"Your file is: {self.random_choice}")
                    # preventing possible crash when the file doesn't exist
                    if exists(self.random_choice):
                        if sys.platform.startswith('linux'):
                            print("opening file with call")
                            subprocess.call(('xdg-open', self.random_choice))
                            #subprocess.Popen([f"xdg-open '{self.random_choice}'"],shell=True)
                        else:
                            os.startfile(self.random_choice)
                    else:
                        # Kind of a bug: this file will be considered as chosen,
                        # even if it doesn't exist.
                        self.textBrowser.setText(f"Wait a moment, the file {self.random_choice} does not exist! Maybe update files?")

#                if (len(difficult_list) - 1) > (current_difficult_piece + 1):
#                    print(len(difficult_list))
#                    # increase current difficult piece count for next selection
#                    current_difficult_piece += 1
#                    difficultPiecesAreOver = "False"

#                else:
#                    self.textBrowser.setText("difficult pieces are over!")
#                    print("difficult pieces are over!")
#                    difficultPiecesAreOver = "True"
            else:
                self.textBrowser.setText("you have not marked any piece as noteworthy yet!")
            print("piece is difficult")
        elif self.isDifficultPiece:
            if not len(difficult_list) == 0:
                print("choosing difficult piece")
                # warning: this is not a real random choice, it is actually a
                # selection of the difficult pieces in a cronological order.
                try:
                     self.random_choice = difficult_list[current_difficult_piece]
                     difficultPiecesAreOver = "False"
                     current_difficult_piece += 1
                except IndexError:
                    print("the difficult pieces are over!!")
                    difficultPiecesAreOver = "True"
                    self.textBrowser.setText("difficult pieces are over!")

                if not difficultPiecesAreOver == "True":
                    # Actual opening of the file: this should be put outside of the if
                    # and should be present only once in the function, but...
                    self.textBrowser.setText(f"Your file is: {self.random_choice}")
                    # preventing possible crash when the file doesn't exist
                    if exists(self.random_choice):
                        if sys.platform.startswith('linux'):
                            print("opening file with call")
                            subprocess.call(('xdg-open', self.random_choice))
                            #subprocess.Popen([f"xdg-open '{self.random_choice}'"],shell=True)
                        else:
                            os.startfile(self.random_choice)
                    else:
                        # Kind of bug: this file will be considered as chosen,
                        # even if it doesn't exist.
                        self.textBrowser.setText(f"Wait a moment, the file {self.random_choice} does not exist! Maybe update files?")

#                if (len(difficult_list) - 1) > (current_difficult_piece + 1):
#                    print(len(difficult_list))
#                    # increase current difficult piece count for next selection
#                    current_difficult_piece += 1
#                    difficultPiecesAreOver = "False"

#                else:
#                    self.textBrowser.setText("difficult pieces are over!")
#                    print("difficult pieces are over!")
#                    difficultPiecesAreOver = "True"
            else:
                self.textBrowser.setText("you have not marked any piece as difficult yet!")
            print("piece is difficult")
        elif self.isRandomNewPiece:
            if not len(all_list) == 0:  # and not isFirstTime
                # if file_path == "":  #directoryNotChosenYet == "True":
                    # self.textBrowser.setText("First you must choose the directory!  fasdfa")
                if not len(already_chosen_list) == 0 and set(all_list) == set(already_chosen_list):
                    self.textBrowser.setText("Files are Over!!!")
                # elif len(added_list) == 0:
                    #self.textBrowser.setText("The chosen directory has no files of that extension 1")
                # if directoryHasNoFiles == "True":
                    # self.textBrowser.setText("The chosen directory has no files of that extension 2")
                elif not len(picker_list) == 0:
                    rand = random.randint(0, len(picker_list) - 1)
                    self.random_choice = picker_list[rand]
                # updating already_chosen_list
                    if self.random_choice in picker_list and not self.random_choice in already_chosen_list:
                        already_chosen_list.append(self.random_choice)
                        print(already_chosen_list)
                        #generate_config_files(already_chosen_filename, already_chosen_list)
                        print("initially picker list is:", picker_list)
                        picker_list.remove(self.random_choice)
                        print("picker list is:", picker_list)



                    # Actual opening of the file: this should be put outside of the if
                    # and should be present only once in the function, but...
                    self.textBrowser.setText(f"Your file is: {self.random_choice}")
                    # preventing possible crash when the file doesn't exist
                    if exists(self.random_choice):
                        if sys.platform.startswith('linux'):
                            print("opening file with call")
                            subprocess.call(('xdg-open', self.random_choice))
                            #subprocess.Popen([f"xdg-open '{self.random_choice}'"],shell=True)
                        else:
                            os.startfile(self.random_choice)
                    else:
                        # Kind of bug: this file will be considered as chosen,
                        # even if it doesn't exist.
                        self.textBrowser.setText(f"Wait a moment, the file {self.random_choice} does not exist! Maybe update files?")



    #             elif all_list == already_chosen_list:  # "Files are Over" in picker_list and
    #                 self.textBrowser.setText("The files are over!")
    #             else:
    #                 if not directoryNotChosenYet == "True" and all_list == already_chosen_list:
    #                     self.textBrowser.setText("The files are over! 1")
    #                     picker_list.append("Files are Over")
    #             # saving picker list
    #            generate_config_files(picker_list_filename, picker_list)
    #            generate_config_files(already_chosen_filename, already_chosen_list)
            else:
                if file_path == "":  #directoryNotChosenYet == "True":
                    self.textBrowser.setText("First you must choose the directory!")
                    #directoryNotChosenYet = "True"
                elif len(already_chosen_list) == 0:
                    self.textBrowser.setText("The directory contains no files with that extension")
                else:
                    self.textBrowser.setText("Files are Over!!!")
        save_configuration()

    def cliccato(self):
        self.update()

    def update_files(self):
        # this should be executed when new files are added/removed
        global file_path, all_list, added_list, picker_list, already_chosen_list, all_list_filename, added_list_filename, picker_list_filename, already_chosen_filename, config, directoryNotChosenYet, directoryHasNoFiles
        read_configuration()
        print ("length of all_list:", len(all_list))
        print ("length of added_list:", len(added_list))
        if not len(all_list) == 0:
            added_list = all_list
        parse_pdf_files()
        # problem: when a new file is added to the collection, everything is reset...
        # testing if there are more or less files than before
        if len(all_list) > len(added_list):
            res = list((Counter(all_list)-Counter(added_list)).elements())
            if not len(res) == 0 and not already_chosen_list == picker_list:
                # problem: editing the picker list somehow prevents the files-are-over detection
                picker_list = picker_list + res
                print("Added Files:", res)
        elif len(all_list) < len(added_list):
            print("some files were removed")
            res = [j for j in added_list if j not in all_list]
            print("Removed files:", res)
            picker_list = [k for k in added_list if k not in res]
        else:
           print("No new files were found")
        save_configuration()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
    form = SightReadingChoicer()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()



#        if exists(picker_list_filename):
#            with open(already_chosen_filename, 'r') as filehandle:
#                already_chosen_list = json.load(filehandle)
#            with open(picker_list_filename, 'r') as filehandle:
#                picker_list = json.load(filehandle)
#                if len(picker_list) == 0:
#                    print("picker list is 0", picker_list)
#                    print("all list: ", all_list)
#                    picker_list = all_list
#                    isFirstTime = True
#        elif "Files are Over" in picker_list:
#            print("picker is over")
#        else:
#            print("picker list is not 0")
        #str_list = [(x[1]) for x in config_items]

#        while True:
#            self.random_choice = get_random_files2(extension)
#            if not(str(self.random_choice) in str_list):
#                break
#            else:
#                print("The files are Over!")

#class classname(QWidget):
#    def __init__(self):
#        QWidget.__init__(self)


#if __name__ == "__main__":
#    app = QApplication([])
#    window = classname()
#    window.show()
#    sys.exit(app.exec_())
