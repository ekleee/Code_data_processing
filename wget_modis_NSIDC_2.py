#!/usr/bin/python
import urllib2
import os
from cookielib import CookieJar
from HTMLParser import HTMLParser

# Define a custom HTML parser to scrape the contents of the HTML data table
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.dataList = []
        self.directory = '/'
        self.indexcol = ';'
        self.Counter = 0
        
    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'table':
            self.Counter += 1
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if self.directory in value or self.indexcol in value:
                        break
                    else:
                        self.inLink = True
                        self.lasttag = tag
                    
    def handle_endtag(self, tag):
            if tag == 'table':
                self.Counter +=1

    def handle_data(self, data):
        if self.Counter == 1:
            if self.lasttag == 'a' and self.inLink and data.strip():
                self.dataList.append(data)
        
parser = MyHTMLParser() 

# Define function for batch downloading
def BatchJob(Files, cookie_jar):
    for dat in Files:
        print "downloading: ", dat
        print '111'
        JobRequest = urllib2.Request(url+dat)
        print '222'
        JobRequest.add_header('cookie', cookie_jar) # Pass the saved cookie into additional HTTP request
        print '333'
        JobRedirect_url = urllib2.urlopen(JobRequest).geturl() + '&app_type=401'
        print '444'

        # Request the resource at the modified redirect url
        Request = urllib2.Request(JobRedirect_url)
        print '555'
        Response = urllib2.urlopen(Request)
        print '666'
        f = open(dat, 'wb')
        print '777'
        f.write(Response.read())
        print '888'
        f.close()
        print '999'
        Response.close()
        print '101010'
    print "Files downloaded to: ", os.path.dirname(os.path.realpath(__file__))

#===============================================================================
# The following code block is used for HTTPS authentication
#===============================================================================

# The user credentials that will be used to authenticate access to the data
username = "your ID"
password = "your password"

# The FULL url of the directory which contains the files you would like to bulk download

for y in range(2003,2018):
    y=str(y)

    for m in range(1,13):
        if m < 10:
            m=str(m)
            m='0'+m
        else:
            m=str(m)

        for d in range(1,32):
            if d < 10:
                d=str(d)
                d='0'+d
            else:
                d=str(d)
            print y+m+d

            url = "https://n5eil01u.ecs.nsidc.org/MOST/MOD29E1D.006/"+y+'.'+m+'.'+d+'/' # Example URL

            print url

# Create a password manager to deal with the 401 reponse that is returned from
# Earthdata Login

            password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
            print '1'
# Create a cookie jar for storing cookies. This is used to store and return
# the session cookie given to use by the data server (otherwise it will just
# keep sending us back to Earthdata Login to authenticate).  Ideally, we
# should use a file based cookie jar to preserve cookies between runs. This
# will make it much more efficient.
 
            cookie_jar = CookieJar()

# Install all the handlers.
            opener = urllib2.build_opener(
                urllib2.HTTPBasicAuthHandler(password_manager),
    #urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
    #urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
                urllib2.HTTPCookieProcessor(cookie_jar))
            urllib2.install_opener(opener)
            print '2'
 
# Create and submit the requests. There are a wide range of exceptions that
# can be thrown here, including HTTPError and URLError. These should be
# caught and handled.

#===============================================================================
# Open a requeset to grab filenames within a directory. Print optional
#===============================================================================

            DirRequest = urllib2.Request(url)
            DirResponse = urllib2.urlopen(DirRequest)

# Get the redirect url and append 'app_type=401'
# to do basic http auth
            DirRedirect_url = DirResponse.geturl()
            DirRedirect_url += '&app_type=401'
            print '3'

# Request the resource at the modified redirect url
            DirRequest = urllib2.Request(DirRedirect_url)
            DirResponse = urllib2.urlopen(DirRequest)

            DirBody = DirResponse.read(DirResponse)

# Uses the HTML parser defined above to pring the content of the directory containing data
            parser.feed(DirBody)
            Files = parser.dataList
            print '4'

# Display the contents of the python list declared in the HTMLParser class
# print Files #Uncomment to print a list of the files

#===============================================================================
# Call the function to download all files in url
#===============================================================================
            print '5'
            print Files
            BatchJob(Files, cookie_jar) # Comment out to prevent downloading to your working directory
            print Files            
print '6'
print 'end'


