from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys,string,random,pyperclip
from cryptography.fernet import Fernet

ui,_ = loadUiType("enc_dec.ui")

class MainApp(QMainWindow,ui):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Encryption/Decryption App")
        self.UI()
        self.Butt_funct()
        self.loaded_key=""
    
    def UI(self):
        style = open("dark_theme.css","r")
        style = style.read()
        self.setStyleSheet(style)
    def Butt_funct(self):
        self.pushButton.clicked.connect(self.generate_pass)
        self.pushButton_2.clicked.connect(self.CTClpBrd)
        self.pushButton_3.clicked.connect(self.generate_key)
        self.pushButton_4.clicked.connect(self.load_key)
        self.pushButton_5.clicked.connect(self.encrypt_pw)
        self.pushButton_6.clicked.connect(self.decrypt_pw)

    def generate_pass(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        pw_length = self.spinBox.value()
        self.generated_pw = ""
        for c in range(pw_length):
            self.generated_pw += random.choice(chars)
        self.textBrowser.setText(self.generated_pw)


    def CTClpBrd(self):
        pw = self.generated_pw
        pyperclip.copy(pw)
        self.label_2.setText('Copied!')

    def generate_key(self):
        file_name = self.lineEdit.text()
        if file_name=="":
            QMessageBox.about(self,"Error","Key file is missing.")
        else:
            key = Fernet.generate_key()
            with open(file_name,"wb") as key_file:
                key_file.write(key)
        self.label_3.setText("Key generated and saved.")

    def load_key(self):
        file_name = self.lineEdit.text()
        if file_name=="":
            QMessageBox.about(self,"Error","Missing file name.")
        else:
            with open(file_name,"rb") as key_file:
                self.loaded_key = key_file.readline()
            self.label_3.setText("Key Loaded and ready to use.")
            

    def encrypt_pw(self):
        if self.loaded_key == "" and self.generated_pw == "":
            QMessageBox.about(self,"Error", "Key or generated password is missing.")
        else:
            encoded_message = self.generated_pw.encode("utf-8")
            f = Fernet(self.loaded_key)
            encrypted_message = f.encrypt(encoded_message)

            file_name = self.lineEdit_2.text()
            with open(file_name,"wb") as encrypted_:
                encrypted_.write(encrypted_message)
            self.label_3.setText("Message encrypted and saved.")

    def decrypt_pw(self):
        
        if self.loaded_key =="" and self.lineEdit_2.text()=="":
            QMessageBox.about(self,'Error','Key or File Name is missing.')
        else:
            f = Fernet(self.loaded_key)
            file_name = self.lineEdit_2.text()
            with open(file_name,"rb") as enc_msg:
                encrypted_msg = enc_msg.readline()
            decrypted_message = f.decrypt(encrypted_msg).decode("utf-8")
            # decoded_message = decoded_message.decode()
            self.textBrowser_2.setText(decrypted_message)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()