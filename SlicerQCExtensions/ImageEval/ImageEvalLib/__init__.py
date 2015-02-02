import os
import sys

__slicer_module__ = os.path.dirname(os.path.abspath(__path__[0]))
print "Path to module: %s" % __slicer_module__

try:
    import requests
except ImportError:
    requestsDir = os.path.join(__slicer_module__, 'Resources', 'Python', 'requests')
    sys.path.append(requestsDir)
    import requests
