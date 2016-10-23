# FB-Message-Analyzer

Run FB-Message-Analyzer in the python interactive mode (v2.7) with your messages.htm file in the same directory to analyze your Facebook messages.

Features include:

1. What time of day does a person send messages? Usage: plottimeofday("John Doe")
2. How many messages has a person sent over time? Usage: plottimeline("John Doe")
3. How positive or negative are a person's messages? Usage: plotsentiments("John Doe")

Note: all these are statistics regarding your interaction with the person (as you only have access to your own messages.htm file). Example: time of day refers to the time of day that person messaged you. Of course, if you analyze yourself, then it is the time of day you sent messages to others.

Packages required:

matplotlib, numpy, lxml, textblob
