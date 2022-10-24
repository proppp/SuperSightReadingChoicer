import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir

class DialogApp(QWidget):
        def __init__(self):
                super().__init__()
                self.resize(800, 600)

                self.button1 = QPushButton('Upload image')
                self.button1.clicked.connect(self.get_image_file)

                self.button2 = QPushButton('Import Python Script')
                self.button2.clicked.connect(self.get_text_file)

                self.labelImage = QLabel()
                self.textEditor = QTextEdit()

                layout = QVBoxLayout()
                layout.addWidget(self.button1)
                layout.addWidget(self.labelImage)
                layout.addWidget(self.button2)
                layout.addWidget(self.textEditor)
                self.setLayout(layout)

        def get_image_file(self):
                file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")
                self.labelImage.setPixmap(QPixmap(file_name))

        def get_text_file(self):
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.AnyFile)
                dialog.setFilter(QDir.Files)

                if dialog.exec_():
                        file_name = dialog.selectedFiles()

                        if file_name[0].endswith('.py'):
                                with open(file_name[0], 'r') as f:
                                        data = f.read()
                                        self.textEditor.setPlainText(data)
                                        f.close()
                        else:
                                pass

if __name__ == '__main__':
        app = QApplication(sys.argv)

        demo = DialogApp()
        demo.show()

        sys.exit(app.exec_())
