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

  def createReviewXML(self, ID, project, label):
    root = et.Element('phd:ImageReview')
    root.attrib = {'ID': ID, 'project': project, 'label': label,
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
    xnatTime = et.SubElement(root, 'xnat:time')
    phdSeriesNumber = et.SubElement(root, 'phd:series_number')
    phdFormDescriptor = et.SubElement(root, 'phd:formdescriptor')
    for questionDict in self.questionsList:
      et.SubElement(phdFormDescriptor, 'phd:field', attrib=questionDict)
    et.dump(root)

  def getQuestionsList(self):
    return self.questionsList
