UsageInfo = """ This script will parse the input configuration
file that contains the file paths required for the BRAINSImageEval
Slicer Module.

Steps:
1) parse through an input configuration file
2) return an object containing a dictionary of the required file paths

"""
import csv

class ParseConfigFile():

  def __init__(self, configFilePath):
    self.configFilePath = configFilePath
    self.makeConfigDict()

  def makeConfigDict(self):
    self.configDict = dict()
    with open(self.configFilePath, 'rU') as csvFile:
      configReader = csv.reader(csvFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
      for row in configReader:
        self.configDict[row[0]] = row[1]

  def getConfigDict(self):
    return self.configDict
