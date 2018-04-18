#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

# HOW TO EXECUTE: 
# python3 xml-parser-barrapunto.py >barrapunto.html
# Next open barrapunto.html file in your navigator")

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib.request import urlopen

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + ".<br/>"
                # To avoid Unicode trouble
                print (line)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print (" Link: " + "<a href=" + self.theContent)
                print (">" + self.theContent + "</a><br/><br/>")
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv)!=1:
    print ("Usage: python3 xml-parser-barrapunto.py >barrapunto.html")
    print ("Next: open barrapunto.html file in your navigator")
    sys.exit(1)
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
print ("<h1>Titulares y links de barrapunto.com</h1>")
url = "http://barrapunto.com/index.rss"
rss = urlopen(url)
html = rss.read().decode("utf-8")  
rss.close()
txt = open('barrapunto.txt', 'w') # Lo introduzco en un txt
txt.write(html)
txt.close()

xmlFile = open('barrapunto.txt', "r")
theParser.parse(xmlFile)
