import urllib
from xml.etree import ElementTree as et

class DataBaseSession():

  def __init__(self):
    hostUrl = "xnat.hdni.org"
    projectReq = "{HOSTURL}/xnat/REST/custom/scans?type=(T1|T2|PD|PDT2)-(15|30)&format=xml".format(HOSTURL=hostUrl)
    print projectReq

    xmlString = self.getXMLstring(projectReq)
    print xmlString

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
