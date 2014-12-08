import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import parseConfigFile
import parseXML
import dataBaseSession

#
# ImageEval
#

class ImageEval(ScriptedLoadableModule):
  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ImageEval" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Testing.TestCases"]
    self.parent.dependencies = []
    self.parent.contributors = ["Jessica Forbes (University of Iowa SINAPSE Lab)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is a scripted loadable module bundled in an extension for the ImageEval Slicer QA Module.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# ImageEvalWidget
#

class ImageEvalWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    self.qtButtonDict = dict()
    # Instantiate and connect widgets ...

    #
    # Reload and Test area
    #
    if True:
        """Developer interface"""
        reloadCollapsibleButton = ctk.ctkCollapsibleButton()
        reloadCollapsibleButton.text = "Advanced - Reload && Test"
        reloadCollapsibleButton.collapsed = False
        self.layout.addWidget(reloadCollapsibleButton)
        reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

        # reload button
        # (use this during development, but remove it when delivering
        #  your module to users)
        self.reloadButton = qt.QPushButton("Reload")
        self.reloadButton.toolTip = "Reload this module."
        self.reloadButton.name = "CardiacAgatstonMeasures Reload"
        reloadFormLayout.addWidget(self.reloadButton)
        self.reloadButton.connect('clicked()', self.onReload)

        # reload and test button
        # (use this during development, but remove it when delivering
        #  your module to users)
        self.reloadAndTestButton = qt.QPushButton("Reload and Test")
        self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
        reloadFormLayout.addWidget(self.reloadAndTestButton)
        self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    # Parses the input configuration file and creates a configDict
    configFilePath = "/IPLlinux/raid0/homes/jforbes/git/WorkInProgress/SlicerQCExtensions/ImageEval/ImageEvalConfigurationFile.csv"
    ParseConfigFileObject = parseConfigFile.ParseConfigFile(configFilePath)
    configDict = ParseConfigFileObject.getConfigDict()

    # Parses the input questionnaire xml file to create questionnaire widgets
    self.questionsList = self.parseQuestionnaireDict(parametersCollapsibleButton, parametersFormLayout,
                                configDict['imageEvalQuestionnaireFilePath'])
    print(self.qtButtonDict)

    # Create database session object to contain scan object for review
    if configDict['dataBase'] == 'XNAT':
      self.localDataBaseSession = dataBaseSession.XNATDataBaseSession(configDict['basePath'], self.questionsList)
    else:
      self.localDataBaseSession = dataBaseSession.DataBaseSession(configDict['basePath'], self.questionsList)
    self.localLogic = ImageEvalLogic()
    self.currentScan = self.localDataBaseSession.getCurrentScan()
    self.localLogic.loadImage(self.currentScan.getFilePath())

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Next")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    #TODO: connect onSelect when any button is selected --> self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    # clears the mrml scene
    slicer.mrmlScene.Clear(0)

  def onSelect(self):
    self.applyButton.enabled = True # TODO add code to check that all boxes are checked before enabling apply button

  def onApplyButton(self):
    logic = ImageEvalLogic()
    print("Run the algorithm")
    logic.run(self.currentScan)
    self.cleanup()

  def addYesNoWidget(self, parametersCollapsibleButton, parametersFormLayout, type, name, tooltip):
    #
    # radio buttons Yes or No
    #
    self.qtButtonDict[(type, name)] = dict()
    self.qtButtonDict[(type, name)]['QFrame'] = qt.QFrame(parametersCollapsibleButton)
    self.qtButtonDict[(type, name)]['QFrame'].setLayout(qt.QHBoxLayout())
    parametersFormLayout.addRow(name, self.qtButtonDict[(type, name)]['QFrame'])
    self.qtButtonDict[(type, name)]['yesRadioButton'] = qt.QRadioButton("Yes", self.qtButtonDict[(type, name)]['QFrame'])
    self.qtButtonDict[(type, name)]['yesRadioButton'].setToolTip(tooltip)
    self.qtButtonDict[(type, name)]['yesRadioButton'].checked = False
    self.qtButtonDict[(type, name)]['QFrame'].layout().addWidget(self.qtButtonDict[(type, name)]['yesRadioButton'])
    self.qtButtonDict[(type, name)]['noRadioButton'] = qt.QRadioButton("No", self.qtButtonDict[(type, name)]['QFrame'])
    self.qtButtonDict[(type, name)]['noRadioButton'].setToolTip(tooltip)
    self.qtButtonDict[(type, name)]['noRadioButton'].checked = False
    self.qtButtonDict[(type, name)]['QFrame'].layout().addWidget(self.qtButtonDict[(type, name)]['noRadioButton'])

  def addRangeWidget(self, parametersFormLayout, type, name, tooltip):
    #
    # slider for Range values
    #
    self.qtButtonDict[(type, name)] = ctk.ctkSliderWidget()
    self.qtButtonDict[(type, name)].singleStep = 1.0
    self.qtButtonDict[(type, name)].minimum = 0.0
    self.qtButtonDict[(type, name)].maximum = 10.0
    self.qtButtonDict[(type, name)].value = 0.0
    self.qtButtonDict[(type, name)].setToolTip(tooltip)
    parametersFormLayout.addRow(name, self.qtButtonDict[(type, name)])

  def addTextEditBoxWidget(self, parametersFormLayout, type, name, tooltip):
    #
    # TextEditBoxWidget
    #
    self.qtButtonDict[(type, name)] = qt.QTextEdit()
    self.qtButtonDict[(type, name)].setToolTip(tooltip)
    parametersFormLayout.addRow(name, self.qtButtonDict[(type, name)])

  def parseQuestionnaireDict(self, parametersCollapsibleButton, parametersFormLayout, imageEvalQuestionnaireFilePath):
    QuestionnaireXMLObject = parseXML.ParseXML(imageEvalQuestionnaireFilePath)
    questionnaireList = QuestionnaireXMLObject.getQuestionsList()
    for questionDict in questionnaireList:
      if questionDict['type'] == 'YesNo':
        self.addYesNoWidget(parametersCollapsibleButton, parametersFormLayout,
                            questionDict['type'], questionDict['name'], questionDict['help'])
      elif questionDict['type'] == 'Range':
        self.addRangeWidget(parametersFormLayout,
                            questionDict['type'], questionDict['name'], questionDict['help'])
      elif questionDict['type'] == 'TextEditor':
        self.addTextEditBoxWidget(parametersFormLayout,
                            questionDict['type'], questionDict['name'], questionDict['help'])
      else:
        print(questionDict)
    return questionnaireList

#
# ImageEvalLogic
#

class ImageEvalLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def run(self, currentScan):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    XnatReviewXMLObject = currentScan.getXnatReviewXMLObject()
    print "*"*50
    print XnatReviewXMLObject.getReviewXMLString()

    return True

  def loadImage(self, path):
    if os.path.exists(path):
      slicer.util.loadVolume(path)

class ImageEvalTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ImageEval1()

  def test_ImageEval1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ImageEvalLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
