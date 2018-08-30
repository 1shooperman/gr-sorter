import urllib2

class Data(object):
    """ Data class for retrieving data from GoodReads """

    def __init__(self, apiUrl):
        self.apiUrl = apiUrl

    def read(self):
        try:
            request = urllib2.urlopen(self.apiUrl)
            #request = urllib2.urlopen"http://localhost:8081")
            body = request.read()
            request.close()
            print "Requesting: %s" % self.apiUrl
            return body
        except IOError:
            print "Error reading URL"
            return None
