from __main__ import qt

class LoginCredentials():

  def __init__(self):
    self.messagePopup = None
    self.createLoginWindow()

  def createLoginWindow(self):
    self.messagePopup = qt.QDialog()
    self.layout = qt.QVBoxLayout()
    self.messagePopup.setLayout(self.layout)

    self.messageLabel = qt.QLabel('Please enter your username and password.\n', self.messagePopup)
    self.usernameLabel = qt.QLabel('username:', self.messagePopup)
    self.passwordLabel = qt.QLabel('password:', self.messagePopup)

    self.messageLabel.setStyleSheet("font-weight: bold")
    self.usernameLabel.setStyleSheet("font-weight: bold")
    self.passwordLabel.setStyleSheet("font-weight: bold")

    self.usernameLine = qt.QLineEdit(self.messagePopup)
    self.passwordLine = qt.QLineEdit(self.messagePopup)

    self.usernameLine.setFixedWidth(100)
    self.passwordLine.setFixedWidth(100)

    self.usernameLine.setText("")
    self.passwordLine.setText("")
    self.passwordLine.setCursorPosition(0)
    self.passwordLine.setEchoMode(2)

    self.layout.addWidget(self.messageLabel)
    self.layout.addWidget(self.usernameLabel)
    self.layout.addWidget(self.usernameLine)
    self.layout.addWidget(self.passwordLabel)
    self.layout.addWidget(self.passwordLine)

    self.okButton = qt.QPushButton("OK")
    self.layout.addWidget(self.okButton)

    self.okButton.connect('clicked()', self.messagePopup.close)

  def openLoginWindow(self):
    self.messagePopup.exec_()

  def getUsername(self):
    return self.usernameLine.text

  def getPassword(self):
    return self.passwordLine.text
