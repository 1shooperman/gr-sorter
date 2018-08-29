import urllib2

try:
    request = urllib2.urlopen("http://localhost:8081")
    body = request.read()
    request.close()
    print body
except IOError:
    print "Error reading URL"
