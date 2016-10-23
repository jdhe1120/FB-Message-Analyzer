import matplotlib.pyplot as pl
import matplotlib.mlab as mlab
import numpy as np
import time
import math
from datetime import datetime, date, timedelta
from collections import Counter
from lxml import etree
from textblob import TextBlob

parser = etree.XMLParser(recover=True)

# helper function to test if something is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

maxnumthreads = ''

# how many threads you want to analyze
while is_number(maxnumthreads) == False:
    try:
        maxnumthreads = int(raw_input("How many threads would you like to analyze? "))
    except:
        print "Please try again."

# helper function to filter out tags of a certain class
def filter_class(root, tag, class_):
    results = [] 
    for div in root.findall(tag):
        if 'class' in div.attrib and div.attrib['class'] == class_:
            results.append(div)
    if len(results) == 1: 
        return results[0]
    else: 
        return results

# file name here
tree = etree.parse('messages.htm',parser=parser)
root = tree.getroot()

# current time
timenow = datetime.now()

# dictionary with key as "name" and value as "time of day message sent"
time_of_day = {}

# dictionary with key as "name" and value as "day number"
day_number = {}

# dictionary with key as "name" and value as "sentiments"
sentiments = {}

# translates a FB message time into a dateTime object
def getTime(string_time):
    return datetime.fromtimestamp(time.mktime(time.strptime(string_time[:-3], "%A, %B %d, %Y at %I:%M%p ")))

body = root.find('body')

for child in body:
    if 'class' in child.attrib and child.attrib['class'] == 'contents':
        contents = child

threads = []

numberthreads = 0

for div in contents:
    for thread in div:
        if numberthreads < maxnumthreads:
            threads.append(thread)
            numberthreads += 1

index = 0

# the main function which gathers character count and time data 
def getInfo(test_case):   
    global index
   
    names =  test_case.text
    if is_number(names[0]):
		names = "Unidentifiable Thread"
    print ("%3s" % str(index)) + '  ' + names
    
    index += 1

    for message in test_case:

        if message.tag == 'div': 
            user = message.find('div').find('span').text
            message_time = filter_class(message.find('div'), 'span', 'meta').text

        if message.tag == 'p':
            if type(message.text) is str:
                if user in sentiments:
                    sentiments[user].append(TextBlob(message.text).sentiment.polarity)
                else:
                    sentiments[user] = [TextBlob(message.text).sentiment.polarity]
                if user in time_of_day:
                    time_of_day[user].append(getTime(message_time).hour)        
                else:
                    time_of_day[user] = [getTime(message_time).hour]

                if user in day_number:
                    day_number[user].append((getTime(message_time) - timenow).days)
                else:
                    day_number[user] = [(getTime(message_time) - timenow).days]

print "Included threads: "

for i in range(len(threads)):
    getInfo(threads[i])

print "Usage: "
print "Histogram of Time of Day Messages sent by John Doe: plottimeofday('John Doe')"
print "Histogram of Messages Sent Over Time by John Doe: plottimeline('John Doe')"
print "Histogram of Sentiments of Messages by John Doe: plotsentiments('John Doe')"

# Makes histogram of times of day of messages sent by a specific person
def plottimeofday(name):
    try:
        x = time_of_day[name]
        pl.title('Histogram of Times of Day of Messages Sent by ' + name)
        pl.hist(x, 23, facecolor='green')
        pl.xlabel('Hour of Day')
        pl.ylabel('Number of Messages Sent')
        pl.xlim([0,24])
        pl.show()
    except KeyError:
		print "The person you entered has never messaged you before."

# Makes histogram of times of day of messages sent by a specific person
def plottimeline(name):
    try:
        x = day_number[name]
        pl.title('Timeline of Messages Sent by ' + name)
        pl.hist(x, (abs(min(x))+1)/7, facecolor='green')
        pl.xlabel('Day Sent')
        pl.ylabel('Number of Messages Sent')
        pl.xlim([min(x),0])
        pl.show()
    except KeyError:
		print "The person you entered has never messaged you before."

# Makes histogram of sentiments of messages sent by a specific person
def plotsentiments(name):
    try:
        x = sentiments[name]
        pl.title('Sentiments of messages sent by ' + name)
        pl.hist(x, 19, facecolor='green')
        pl.xlabel('Sentiment Level (1: Positive, -1: Negative')
        pl.ylabel('Number of Messages Sent')
        pl.xlim([-1,1])
        pl.show()
    except KeyError:
		print "The person you entered has never messaged you before."
