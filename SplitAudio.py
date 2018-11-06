# This script needs two things: pydub and libav.
# pydub can be installed via CLI/PowerShell by typing 'pip install pydub'.
# pydub needs libav to modify audio; this needs to be placed in Python's active path variable;
# since we are using a virtual Python environment, it is automatically loaded internally for this script.

# Pydub GITHUB Source: https://github.com/jiaaro/pydub

from pydub import AudioSegment

# This converts a timestamp into a millisecond measure when given a string in the format
# MM:SS-MM-SS, where the first bit is the start, and the second is the ending of the track.
# Since pydub operates in millisecond measures, the timestamp must be converted at both the start and endpoints.
# The formula is ( (minutes * 60) + (seconds) ) * 1000.
def convertToMilliseconds(rawString):
    parsedstring = rawString.split("-")
    parsedstring = [parsedstring[0], parsedstring[1]]
    startend = []

    for item in parsedstring:
        item = item.split(":")
        item = ( (int(item[0]) * 60) + int(item[1]) ) * 1000
        startend.append(item)

    return tuple(startend)

# This uses ripped audio from a BenMarshall01 YouTube video as a proof-of-concept.
path = "<SOMEPATH>\\Halo Reach Complete Soundtrack 14 - Firefight.mp3"

# Use a dictionary to store the track information, their start and end-times.
tracks = {
    "Intro 1: Orbital Defense" : "0:00-0:27",
    "Fall From Grace (Alternate)" : "0:28-2:58",
    "Sword Control (Percussion Only)" : "2:59-5:03",
    "Intro 2: Descent" : "5:04-5:31",
    "Library Suite 2.0" : "5:32-7:52",
    "Second Wave (Percussion Only)" : "7:53-10:15",
    "Intro 3: Whispers" : "10:16-10:42",
    "We All Got Secrets" : "10:43-12:51",
    "The Sky's No Limit" : "12:52-14:38",
    "Intro 4: The Ardent Prayer" : "14:39-15:07",
    "Recon" : "15:08-19:09",
    "Powder Keg" : "19:10-21:14",
    "Intro 5: Keep Your Eyes Open" : "21:15-21:42",
    "War Machine" : "21:43-24:34",
    "The End of the World (Percussion Only)" : "24:35-26:35"
}

# Use pydub/AudioSegment to import the audio file.
Sound = AudioSegment.from_file(path)

# Use the information stored in the dictionary to grab the soundbites and export them.

counter = 0
for key, val in tracks.items():
    Filepath = "<SOMEDESTINATION>\\%d_%s.mp3" % (counter, key.replace(":"," -"))
    Timestamps = convertToMilliseconds(val)

    soundbite = Sound[Timestamps[0]:Timestamps[1]]
    soundbite.export(Filepath,format="mp3")

    counter += 1

    print("Filename:%s\nTimeStamps:%s\n" % (Filepath, Timestamps))
