import urllib
import os
import time

directory = 'DIRECTORY_HERE'

startComicCounter = (len(os.listdir(directory)) / 2) + 1
comicCounter = startComicCounter
if comicCounter > 403:
    comicCounter = comicCounter + 1

print "Number Downloaded: " + str(comicCounter - 1)

def download_comic(url, comicName):
    print url
    print comicName
    image = urllib.URLopener()
    image.retrieve(url, directory + comicName)

def title(source, titleType):
    # Title Type 1 is the standard HTML title
    # Title Type 2 is the comic title
    
    if titleType == 1:
        titleStart = source.lower().find('<title>')
        titleEnd = source.lower().find('</title>', titleStart + 1)
        title = source[titleStart + 7:titleEnd]
    else:
        titleStart = source.lower().find('<div id="ctitle">')
        titleEnd = source.lower().find('</div>', titleStart + 1)
        title = source[titleStart + 17:titleEnd]
        title = unescape(title)
    
    return title

def comic_title(comicNumber):
    comicString = str(comicNumber)
    while len(comicString) < 5:
        comicString = '0' + comicString
    return comicString

def unescape(text):
    return text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")

def title_text(source, comicLocation):
    titleStart = source.lower().find('<img', comicLocation)
    titleStart = source.lower().find('title="', titleStart) + 7
    titleEnd = source.lower().find('"', titleStart)
    return unescape(source[titleStart:titleEnd])

def transcript(source):
    transcriptid = '<div id="transcript" style="display: none">'
    tranStart = source.lower().find(transcriptid) + len(transcriptid)
    tranEnd = source.lower().find('</div>', tranStart)
    return unescape(source[tranStart:tranEnd])

def isLarge(url):
    return title(urllib.urlopen(url + '/large/').read(), 1) != '404 - Not Found'

def sumlist(time):
    zeroes = 0
    summation = 0
    for entry in time:
        if entry == 0:
            zeroes = zeroes + 1
        else:
            summation = summation + entry
    summation = 10 * summation / (10 - zeroes)
    return summation

    
print "Determining number of comics..."

i = 1137
tempURL = "http://xkcd.com/" + str(i)
tempSource = urllib.urlopen(tempURL).read()
tempTitle = title(tempSource, 1)
while tempTitle != "404 - Not Found":
    i = i + 1
    tempURL = "http://xkcd.com/" + str(i)
    tempSource = urllib.urlopen(tempURL).read()
    tempTitle = title(tempSource, 1)
    print i
totalComics = i - 1
print "Total Comics: " + str(totalComics)

startTime = time.time()

zerotime = startTime - startTime

timelist = [zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime]

while True:
    if comicCounter == 404:
        comicCounter = 405
    
    url = "http://xkcd.com/" + str(comicCounter)
    pageSource = urllib.urlopen(url).read()

    n = 0
    while title(pageSource, 1) != '404 - Not Found':
        pageSource = urllib.urlopen(url).read()
        if n > 5:
            break
        n = n + 1
    
    if title(pageSource, 1) != "404 - Not Found":
        comicLocation = pageSource.lower().find('<div id="comic">')
        if pageSource.lower().find('<a href="', comicLocation) < pageSource.lower().find('<img src="', comicLocation) and isLarge(url):
            largeurl = url + '/large/'
            largeSource = urllib.urlopen(largeurl).read()
            linkStart = largeSource.lower().find('src="') + 5
            linkEnd = largeSource.lower().find('">', linkStart)
            download_comic(largeSource[linkStart:linkEnd], comic_title(comicCounter) + '.png')
        else:
            linkStart = pageSource.lower().find('<img src="', comicLocation)
            linkEnd = pageSource.lower().find('"', linkStart + 10)
            download_comic(pageSource[linkStart + 10:linkEnd], comic_title(comicCounter) + '.png')
        textFile = open(directory + comic_title(comicCounter) + '.txt', 'w')
        fileString = 'Comic Title: ' + title(pageSource, 2) + '\n' * 2
        fileString = fileString + 'Title Text: ' + title_text(pageSource, comicLocation) + '\n' * 2
        fileString = fileString + 'Transcript: ' + transcript(pageSource)
        textFile.write(fileString)
    else:
        break

    print "Comics Completed: " + str(comicCounter)
    timeTaken = time.time() - startTime
    startTime = time.time()
    print "Time Taken: " + str(timeTaken)
    timelist[comicCounter % 10] = timeTaken
    timeRemaining = (sumlist(timelist)) * (totalComics - comicCounter) / 10
    print "Estimated Time Remaining: " + str(timeRemaining)
    
    comicCounter = comicCounter + 1

print "Finished"
