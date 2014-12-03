UsageInfo = """ This script will parse the XML input configuration
file that contains the questionnaire for the BRAINSImageEval
Slicer Module.

Steps:
1) parse through an input XML file using xml.etree
2) return an object containing the questions, question type, default values, etc.

Example file to parse: /IPLlinux/raid0/homes/jforbes/git/WorkInProgress/
SlicerQCExtensions/ImageEval/ImageEvalQuestionnaire.xml

"""

from xml.etree import ElementTree as et

class ParseXML():

  def __init__(self, imageEvalQuestionnaireFilePath):
    self.imageEvalQuestionnaireFilePath = imageEvalQuestionnaireFilePath
    self.makeQuestionsList()

  def getXMLstring(self):
    with open(self.imageEvalQuestionnaireFilePath, 'rU') as handle:
      xmlString = handle.read()
    return xmlString

  def makeQuestionsList(self):
    xmlString = self.getXMLstring()
    root = et.fromstring(xmlString)
    self.questionsList = list()
    formDescriptor = root.find('{http://nrg.wustl.edu/phd}formdescriptor')
    for child in formDescriptor.getchildren():
      attribDict = child.attrib
      if 'type' in attribDict.keys():
        self.questionsList.append(attribDict)

  def getQuestionsList(self):
    return self.questionsList
