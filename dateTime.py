'''Global values for dateTime'''
monthList = [None, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
monthListAbbrv = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
dayList = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class dateTime:
	
	'''Constructor: This will take in the original string, and nothing else. values will be set to 'None' '''
	def __init__(self,string):
		self.month = None
		self.date = None
		self.day = None
		self.year = None
		self.week = None
		self.hour = None
		self.minute = None
		self.second = None
		self.type = None
		self.originalString = string
		self.dateString = None
		#Determine the type of stored information to fill out the data sheet.
		self.determineType()
		
	def __repr__(self):
		return self.originalString
	
	'''Main workhorse constructor: this will attempt to identify the type of data stored, and then classify the information accordingly.'''
	def determineType(self):
		
		#If there is a timestamp included, then split the string into two parts, and assign accordingly.
		if "T" in self.originalString and "P" not in self.originalString:
			tempList = self.originalString.split("T")
			self.dateString = tempList[0]
			self.timeString = tempList[1]
			
		#Durations will contain a "P" in the beginning.
		elif "T" in self.originalString and "P" in self.originalString:
			self.type = "Duration"
			#Keep a deep copy of the original string to do a comprehension.
			#This removes the characters from the period and sends them to a list so the numbers can be directly addressed.
			stringCopy = self.originalString[::]
			periodDurChars = ["P", "Y", "M", "D", "T", "H", "M", "S"]
			for char in periodDurChars:
				stringCopy = stringCopy.replace(char, " ")
			stringCopy = stringCopy.strip()
			stringCopy = stringCopy.split(" ")
			stringCopy.remove('')
			self.year = int(stringCopy[0])
			self.month = int(stringCopy[1])
			self.day = int(stringCopy[2])
			self.hour = int(stringCopy[3])
			self.minute = int(stringCopy[4])
			self.second = int(stringCopy[5])
			return
		
		else:
			self.dateString = self.originalString
		#Check if there are hyphens contained within the string.
		if "-" in self.dateString:
			
			#This is a special case where we catch calendar dates of format "--MM-DD" or "--MMDD"
			if self.dateString[0:2] == "--":
				self.type = "Calendar Date"
				self.month = int(self.dateString[2:4])
				if self.originalString[4:5] == "-":
					self.date = int(self.dateString[5::])
				else:
					self.date = int(self.dateString[4::])
				return
			
			#Convert the string into a list, using the hyphens as the delimiter.
			stringSplit = self.dateString.split("-")
			
			#Week Dates are identified by a "W" present.
			if "W" in self.dateString:
				self.type = "Week Date"
				self.year = int(stringSplit[0])
				self.week = int(stringSplit[1][1::])
				try:
					self.day = int(stringSplit[2])
				except IndexError:
					self.day = None
				return
			#Otherwise, it is a regular calendar date.
			else:
				self.type = "Calendar Date"
				self.year = int(stringSplit[0])
				self.month = int(stringSplit[1])
				#Add the date if there is one present; ignore if there isn't.
				try:
					self.date = int(stringSplit[2])
				except IndexError:
					self.date = None
				return
				
		#For dates with no hyphenation.
		else:
			#Catch date types of YYYY or YYYYMM.
			if len(self.originalString) == 4 or len(self.dateString) == 6:
				self.type = "Calendar Date"
				self.year = int(self.dateString[0:4])
				try:
					self.month = int(self.dateString[4::])
				except ValueError:
					self.month = None
				return
			
			#Catch date types of DDMMMYY, by checking if there is a month contained in the MMM.
			elif self.originalString[2:5] in monthListAbbrv:
				self.type = "Calendar Date"
				self.date = int(self.dateString[0:2])
				self.month = int(monthListAbbrv.index(self.dateString[2:5]))
				
				#If there are any dates greater than 18, it's probably before the 21st century, so adjust accordingly.
				if int(self.dateString[5::]) > 18:
					self.year = int("19" + self.dateString[5::])
				else:
					self.year = int("20" + self.dateString[5::])
				return
			
			#Catch date types of YYYYWwwD, where 'ww' is the numeric value of the week, from 0 to 52.
			elif "W" in self.dateString:
				self.type = "Week Date"
				self.year = int(self.dateString[0:4])
				self.week = int(self.dateString[6:7])
				self.day = int(self.dateString[7::])
		
		return
	
	def getInfo(self):
		returnString = ""
		if self.originalString != None:
			returnString += "Original String: '%s'\n" % (self.originalString)
		if self.type != None:
			returnString += "Type: %s\n" % (self.type)
		if self.type == None:
			returnString += "Type: UNKNOWN\n"
		if self.year != None:
			returnString += "Year: %s\n" % (self.year)
		if self.month != None:
			returnString += "Month: %s\n" % (self.month)
		if self.week != None:
			returnString += "Week: %s\n" % (self.week)
		if self.date != None:
			returnString += "Date: %s\n" % (self.date)			
		if self.day != None:
			returnString += "Day: %s\n" % (self.day)
		if self.hour != None:
			returnString += "Hour: %s\n" % (self.hour)
		if self.minute != None:
			returnString += "Minute: %s\n" % (self.minute)
		if self.second != None:
			returnString += "Second: %s\n" % (self.second)
		return returnString


dateTimeList = []
#Cleaning - this will accept a CSV, and convert it into a list object; the for-loop will remove any newline statements from the dateList.
with open("test01.csv") as f:
	dateList = f.readlines()

for i in range(len(dateList)):
	dateList[i] = dateList[i].rstrip('\r\n')
	if len(dateList[i]) < 4:
		continue
	dateTimeList.append(dateTime(dateList[i]))

for x in dateTimeList:
	print(x.getInfo())
