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
from datetime import datetime

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


class ReviewXML():

  def __init__(self, project, label, seriesnumber, questionsList):
    self.project = project
    self.label = label
    self.seriesnumber = seriesnumber
    self.questionsList = questionsList
    self.root = self.createReviewXML()

  def createReviewXML(self):
    pass

  def getReviewXMLString(self):
    return et.tostring(self.root)

  def getReviewXMLRootElement(self):
    return self.root

  def printReviewXMLStringToFile(self, filename):
    with open(filename, 'w') as handle:
      handle.write(self.getReviewXMLString())

class XnatReviewXML(ReviewXML):

  def createReviewXML(self):
    root = et.Element('phd:ImageReview')
    root.attrib = {'ID': '', 'project': self.project, 'label': self.label,
                   'xmlns:arc':"http://nrg.wustl.edu/arc", 'xmlns:val':"http://nrg.wustl.edu/val",
                   'xmlns:pipe':"http://nrg.wustl.edu/pipe", 'xmlns:fs':"http://nrg.wustl.edu/fs",
                   'xmlns:wrk':"http://nrg.wustl.edu/workflow", 'xmlns:scr':"http://nrg.wustl.edu/scr",
                   'xmlns:xdat':"http://nrg.wustl.edu/security", 'xmlns:cat':"http://nrg.wustl.edu/catalog",
                   'xmlns:phd':"http://nrg.wustl.edu/phd", 'xmlns:prov':"http://www.nbirn.net/prov",
                   'xmlns:xnat':"http://nrg.wustl.edu/xnat", 'xmlns:xnat_a':"http://nrg.wustl.edu/xnat_assessments",
                   'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance",
                   'xsi:schemaLocation':"http://nrg.wustl.edu/fs " \
                       "https://xnat.hdni.org/xnat/schemas/fs/fs.xsd " \
                       "http://nrg.wustl.edu/workflow " \
                       "https://xnat.hdni.org/xnat/schemas/pipeline/workflow.xsd " \
                       "http://nrg.wustl.edu/catalog " \
                       "https://xnat.hdni.org/xnat/schemas/catalog/catalog.xsd " \
                       "http://nrg.wustl.edu/pipe " \
                       "https://xnat.hdni.org/xnat/schemas/pipeline/repository.xsd " \
                       "http://nrg.wustl.edu/scr " \
                       "https://xnat.hdni.org/xnat/schemas/screening/screeningAssessment.xsd " \
                       "http://nrg.wustl.edu/arc " \
                       "https://xnat.hdni.org/xnat/schemas/project/project.xsd " \
                       "http://nrg.wustl.edu/val " \
                       "https://xnat.hdni.org/xnat/schemas/validation/protocolValidation.xsd " \
                       "http://nrg.wustl.edu/xnat " \
                       "https://xnat.hdni.org/xnat/schemas/xnat/xnat.xsd " \
                       "http://nrg.wustl.edu/phd " \
                       "https://xnat.hdni.org/xnat/schemas/phd/phd.xsd " \
                       "http://nrg.wustl.edu/xnat_assessments " \
                       "https://xnat.hdni.org/xnat/schemas/assessments/assessments.xsd " \
                       "http://www.nbirn.net/prov " \
                       "https://xnat.hdni.org/xnat/schemas/birn/birnprov.xsd " \
                       "http://nrg.wustl.edu/security " \
                       "https://xnat.hdni.org/xnat/schemas/security/security.xsd"}
    xnatDate = et.SubElement(root, 'xnat:date')
    xnatDate.text = datetime.now().strftime("%Y-%m-%d")
    xnatTime = et.SubElement(root, 'xnat:time')
    xnatTime.text = datetime.now().strftime("%H:%M:%S")
    phdSeriesNumber = et.SubElement(root, 'phd:series_number')
    phdSeriesNumber.text = self.seriesnumber
    phdFormDescriptor = et.SubElement(root, 'phd:formdescriptor')
    for questionDict in self.questionsList:
      et.SubElement(phdFormDescriptor, 'phd:field', attrib=questionDict)
    #et.dump(root)
    return root

  def setFieldVariableValue(self, name, result):
    for child in self.root.iter('phd:field'):
      if str(child.attrib['name']) == str(name):
        child.set('value', result)
