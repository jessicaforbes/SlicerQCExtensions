import urllib
from xml.etree import ElementTree as et

class DataBaseSession():

  def __init__(self):
    # hostUrl = "xnat.hdni.org"
    # projectReq = "{HOSTURL}/xnat/REST/custom/scans?type=(T1|T2|PD|PDT2)-(15|30)&format=xml".format(HOSTURL=hostUrl)
    # print projectReq
    #
    # xmlString = self.getXMLstring(projectReq)
    # print xmlString

    self.notReviewedList = self.createUnreviewedScansList(xmlString)
    self.reviewedList = list()
    print self.notReviewedList

  def getXMLstring(self, restURL):
    """
    Copy the Image Eval XML information from XNAT.
    Store it in the string "xmlString"
    """
    opener = urllib.FancyURLopener({})
    username, pword = opener.prompt_user_passwd("www.predict-hd.net/xnat", "XNAT")
    url = "https://{0}:{1}@{2}".format(username, pword, restURL)
    info = urllib.urlopen(url)
    xml_string = info.read()
    return xml_string

  def createUnreviewedScansList(self, xmlString):
    root = et.fromstring(xmlString)
    notReviewedList = list()
    columnList = self.getColumnList(root)
    for row in root.iter('row'):
      reviewed = row[10].text
      scan = XNATScanObject(row, columnList)
      print scan.getSession()
      if reviewed != 'Yes':
        notReviewedList.append(row)
    return notReviewedList

  def getColumnList(self, root):
    columnList = list()
    columnElements = root.findall('results/columns/column')
    for elem in columnElements:
      columnList.append(elem.text)
    return columnList

  def getUnreviewedScan(self):
    if len(self.notReviewedList) == 0:
      return False
    else:
      val = self.notReviewedList.pop(0)
      self.reviewedList.append(val)
      return val


class ScanObject():

  def __init__(self, element):
    self.parseXMLElement()

  def getSession(self):
    return self.session


class XNATScanObject(ScanObject):

  def __init__(self, rowElement, columnList):
    self.rowElement = rowElement
    self.columnList = columnList
    self.parseXML()

  def parseXML(self):
    self.project = self.setVariable('project')
    self.subject_id = self.setVariable('subject_id')
    self.subject = self.setVariable('subject')
    self.sessionID = self.setVariable('session_id')
    self.session = self.setVariable('session')
    self.date = self.setVariable('date')
    self.time = self.setVariable('time')
    self.seriesnumber = self.setVariable('seriesnumber')
    self.type = self.setVariable('type')
    self.quality = self.setVariable('quality')
    self.reviewed = self.setVariable('reviewed')
    self.status = self.setVariable('status')
    self.element_name = self.setVariable('element_name')
    self.insert_date = self.setVariable('insert_date')
    self.activation_date = self.setVariable('activation_date')
    self.last_modified = self.setVariable('last_modified')

  def setVariable(self, val):
    i = self.columnList.index(val)
    return self.rowElement[i].text

if __name__ == "__main__":
  Object = DataBaseSession()
  unreviewedScan = Object.getUnreviewedScan()
  print unreviewedScan
