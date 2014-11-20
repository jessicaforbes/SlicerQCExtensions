import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

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

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    #TODO: connect onSelect when any button is selected --> self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    self.parseQuestionnaireDict(parametersCollapsibleButton, parametersFormLayout)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = True # TODO add code to check that all boxes are checked before enabling apply button

  def onApplyButton(self):
    logic = ImageEvalLogic()
    print("Run the algorithm")
    logic.run()

  def addYesNoWidget(self, parametersCollapsibleButton, parametersFormLayout, name, tooltip):
    #
    # radio buttons Yes or No
    #
    self.RadioButtonsFrame = qt.QFrame(parametersCollapsibleButton)
    self.RadioButtonsFrame.setLayout(qt.QHBoxLayout())
    parametersFormLayout.addRow(name, self.RadioButtonsFrame)
    self.yes = qt.QRadioButton("Yes", self.RadioButtonsFrame)
    self.yes.setToolTip(tooltip)
    self.yes.checked = False
    self.RadioButtonsFrame.layout().addWidget(self.yes)
    self.no = qt.QRadioButton("No", self.RadioButtonsFrame)
    self.no.setToolTip(tooltip)
    self.no.checked = False
    self.RadioButtonsFrame.layout().addWidget(self.no)

  def addRangeWidget(self, parametersFormLayout, name, tooltip):
    #
    # slider for Range values
    #
    self.rangeSliderWidget = ctk.ctkSliderWidget()
    self.rangeSliderWidget.singleStep = 1.0
    self.rangeSliderWidget.minimum = 0.0
    self.rangeSliderWidget.maximum = 10.0
    self.rangeSliderWidget.value = 0.0
    self.rangeSliderWidget.setToolTip(tooltip)
    parametersFormLayout.addRow(name, self.rangeSliderWidget)

  def parseQuestionnaireDict(self, parametersCollapsibleButton, parametersFormLayout):
    questionnaireList = [{'type': 'YesNo', 'name': 'Normal variants', 'value': 'No', 'help': 'Does the image show normal variants?'}, {'type': 'YesNo', 'name': 'Lesions', 'value': 'No', 'help': 'Does the image show lesions?'}, {'type': 'Range', 'name': 'SNR', 'value': '8', 'help': 'Overall SNR weighted images 0=bad 10=good'}, {'type': 'Range', 'name': 'CNR', 'value': '8', 'help': 'Overall CNR weighted images 0=bad 10=good'}, {'type': 'YesNo', 'name': 'Full Brain Coverage', 'value': 'Yes', 'help': 'Is the whole brain visible in the image?'}, {'type': 'YesNo', 'name': 'Misalignment', 'value': 'No', 'help': 'Does the image show misalignment?'}, {'type': 'YesNo', 'name': 'Swap / Wrap Around', 'value': 'No', 'help': 'Does the image show swap / wrap around?'}, {'type': 'YesNo', 'name': 'Ghosting / Motion', 'value': 'No', 'help': 'Are there motion artifacts in the image?'}, {'type': 'YesNo', 'name': 'Inhomogeneity', 'value': 'No', 'help': 'Does the image show Inhomgeneity?'}, {'type': 'YesNo', 'name': 'Susceptibility/Metal', 'value': 'No', 'help': 'Does the image show susceptibility?'}, {'type': 'YesNo', 'name': 'Flow artifact', 'value': 'No', 'help': 'Does the image show flow artifact?'}, {'type': 'YesNo', 'name': 'Truncation artifact', 'value': 'No', 'help': 'Does the image show truncation?'}, {'type': 'Range', 'name': 'overall QA assessment', 'value': '8', 'help': '0=bad 10=good'}, {'type': 'String', 'name': 'Evaluator', 'value': 'joneskl', 'help': 'Name of person evalating this scan'}, {'type': 'String', 'name': 'Image File', 'value': '/hjohnson/TrackOn/HDNI_004/349964982/349964982_20130624_30/ANONRAW/349964982_349964982_20130624_30_T1-30_301.nii.gz', 'help': 'Name of the image file being evaluated'}, {'type': 'TextEditor', 'name': 'Free Form Notes', 'value': ' ', 'help': 'Mention anything unusual or significant about the images here'}, {'type': 'YesNo', 'name': 'Evaluation Completed', 'value': 'Yes', 'help': 'Is the evaluation completed? (No implies further evaluation needed)'}]
    for val in questionnaireList:
      questionDict = val
      if questionDict['type'] == 'YesNo':
        self.addYesNoWidget(parametersCollapsibleButton, parametersFormLayout,
                            questionDict['name'], questionDict['help'])
      elif questionDict['type'] == 'Range':
        self.addRangeWidget(parametersFormLayout,
                            questionDict['name'], questionDict['help'])

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

  def run(self):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    return True


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
