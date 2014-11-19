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
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.outputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)


    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # scale factor for screen shots
    #
    self.screenshotScaleFactorSliderWidget = ctk.ctkSliderWidget()
    self.screenshotScaleFactorSliderWidget.singleStep = 1.0
    self.screenshotScaleFactorSliderWidget.minimum = 1.0
    self.screenshotScaleFactorSliderWidget.maximum = 50.0
    self.screenshotScaleFactorSliderWidget.value = 1.0
    self.screenshotScaleFactorSliderWidget.setToolTip("Set scale factor for the screen shots.")
    parametersFormLayout.addRow("Screenshot scale factor", self.screenshotScaleFactorSliderWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    self.parseQuestionnaireDict(parametersCollapsibleButton, parametersFormLayout)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = ImageEvalLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    screenshotScaleFactor = int(self.screenshotScaleFactorSliderWidget.value)
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), enableScreenshotsFlag,screenshotScaleFactor)

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

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == -1:
      # full window
      widget = slicer.util.mainWindow()
    elif type == slicer.qMRMLScreenShotDialog().FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog().ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog().Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog().Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog().Green:
      # green slice window
      widget = lm.sliceWidget("Green")

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, self.screenshotScaleFactor, imageData)

  def run(self,inputVolume,outputVolume,enableScreenshots=0,screenshotScaleFactor=1):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    self.enableScreenshots = enableScreenshots
    self.screenshotScaleFactor = screenshotScaleFactor

    self.takeScreenshot('ImageEval-Start','Start',-1)

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
