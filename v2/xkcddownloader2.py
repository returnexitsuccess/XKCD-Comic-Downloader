import urllib
import os
import time

def getAttr(source, attr):
    attrStart = source.lower().find('"' + attr.lower() + '": ')
    attrStart = source.lower().find(": ", attrStart) + 2
    attrEnd = source.lower().find(', "', attrStart)
    returnValue = source[attrStart:attrEnd].replace('"', '')
    if (returnValue == ""):
        return "NONE"
    return returnValue

def comicTitle(comicNumber):
    comicString = str(comicNumber)
    while len(comicString) < 5:
        comicString = '0' + comicString
    return comicString

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


directory = 'DIRECTORY_HERE'
# Example C:/pics/xkcd/ make sure to include slash at end

comicCounter = (len(os.listdir(directory)) / 2)
if comicCounter > 403:
    comicCounter = comicCounter + 1

print "Number Downloaded: " + str(comicCounter)

comicCounter += 1
totalComics = int(getAttr(urllib.urlopen("http://xkcd.com/info.0.json").read(), "num"))
print totalComics

startTime = time.time()

zerotime = startTime - startTime

timelist = [zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime, zerotime]

while (comicCounter <= totalComics):
    if (comicCounter == 404):
        comicCounter += 1

    url = "http://xkcd.com/" + str(comicCounter) + "/info.0.json"
    pageSource = urllib.urlopen(url).read()
    comicName = comicTitle(comicCounter)
    
    imgURL = getAttr(pageSource, "img").replace('\\', '')
    print imgURL
    image = urllib.URLopener()
    try:
        image.retrieve(imgURL, directory + comicName + '.png')
    except IOError:
        print "IOError for comic number " + str(comicCounter)
    
    textFile = open(directory + comicName + '.txt', 'w')
    fileString = 'Comic Title: ' + getAttr(pageSource, "title") + ('\n' * 2)
    fileString += 'Title Text: ' + getAttr(pageSource, "alt") + ('\n' * 2)
    fileString += 'Transcript: ' + getAttr(pageSource, "transcript")
    textFile.write(fileString)
    textFile.close()

    print "Comics Completed: " + str(comicCounter)
    
    timeTaken = time.time() - startTime
    startTime = time.time()
    print "Time Taken: " + str(timeTaken)
    timelist[comicCounter % 10] = timeTaken
    timeRemaining = (sumlist(timelist)) * (totalComics - comicCounter) / 10
    print "Estimated Time Remaining: " + str(timeRemaining) + "\n"

    comicCounter += 1

print "Finished"
raw_input()
