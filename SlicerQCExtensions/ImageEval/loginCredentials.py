from __main__ import qt

class LoginCredentials():

  def __init__(self):
    self.defaultUsernameText = 'username'
    self.defaultPasswordText = 'password'
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

    self.usernameLine.setText(self.defaultUsernameText)
    self.passwordLine.setStyleSheet("color: lightgray")
    self.passwordLine.setText(self.defaultPasswordText)
    self.passwordLine.setCursorPosition(0)

    self.layout.addWidget(self.messageLabel)
    self.layout.addWidget(self.usernameLabel)
    self.layout.addWidget(self.usernameLine)
    self.layout.addWidget(self.passwordLabel)
    self.layout.addWidget(self.passwordLine)

    self.okButton = qt.QPushButton("OK")
    self.layout.addWidget(self.okButton)

    self.okButton.connect('clicked()', self.messagePopup.close)
    self.usernameLine.connect('cursorPositionChanged(int, int)', self.onUsernameLineFocused)
    self.passwordLine.connect('cursorPositionChanged(int, int)', self.onPasswordLineFocused)

  def openLoginWindow(self):
    self.messagePopup.exec_()

  def onUsernameLineFocused(self):
    if self.defaultUsernameText in str(self.usernameLine.text):
      self.usernameLine.setText("")

  def onPasswordLineFocused(self):
    if self.defaultPasswordText in str(self.passwordLine.text):
      self.passwordLine.setText("")
      self.passwordLine.setStyleSheet("color: black")
      self.passwordLine.setEchoMode(2)

  def getUsername(self):
    return self.usernameLine.text

  def getPassword(self):
    return self.passwordLine.text
