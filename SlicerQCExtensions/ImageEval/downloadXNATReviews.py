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

if __name__ == "__main__":
  Object = DataBaseSession()
  unreviewedScan = Object.getUnreviewedScan()
  print unreviewedScan
