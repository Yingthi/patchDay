import datetime
import calendar

import win32com.client
from win32com.client import Dispatch, constants

#program for maintaining and optimizing a patch medication schedule.
#see README

class Patch:

    def __init__(self, loc, LoR, day, time, year, month, dayN):

        #the time and the day are automatically formatted during init
        #however, they need to be 'set' for past patches
        self.location = loc

        #LoR mean "Left or Right"
        self.LoR = LoR
        
        self.day = day
        self.time = time

        #attributes for using 'date' object
        self.year = int(year)
        self.month = int(month)
        self.dayN = int(dayN)
        self.date = datetime.date(self.year,self.month,self.dayN)

        #attributes for creating now object
        self.hour = int(self.time[:2])
        self.minute = int(self.time[3:])
        
        self.datetime = datetime.datetime(self.year,self.month,
        self.dayN,self.hour,self.minute)

    def __repr__(self):
        return(self.LoR + ' ' + self.location +
        ' ' + self.day + ' ' + self.time)

    def __str__(self):
        return str((self.LoR + ' ' + self.location +
        ' ' + self.day + ' ' + self.time))

    def getTime(self):
        return self.now

    def getLocation(self):
        return self.location

    def getNextPatch(self):
        return self.nextPatchDate

    def getLoR(self):
        return self.LoR

    def setLocation(self,loc):
        self.location = loc

    def setLoR(self,lor):
        self.LoR = lor

    def setTime(self,time):
        #please enter exact format: a str object like '04:41'
        self.time = time

    def setDayN(self,dayN):
        self.dayN = dayN

    def setDay(self,day):
        self.day = day

    def setMonth(self,month):
        self.month = month

    def setYear(self,year):
        self.year = year

    def halfweek_plus(self):
        #adds 3.5 days for determing next patch
        #used for reminder and changing patch functions

        #Vivelle patches are changed twice a week (3.5 days)
        delta = datetime.timedelta(days=3,hours=12)
        nextDate = self.datetime + delta
        day = calendar.day_name[nextDate.weekday()]
        time = str(nextDate)[11:16]
        p1 = "Change " + "'" + self.LoR + "'" + " patch on your "
        p2 = ("'" + self.location + "'" +
        " on " + day + ' at ' + time + '.')
        return(p1 + p2)
    

#Psched = Patch Schedule
class Psched:

    #initialize the schedule with current patches on skin
    def __init__(self):

        #looks at CSV for current data
        try:
            self.datafile = open("patchdata.csv",'r')
            self.datafile.close()
            
        #if not data exists, make a new blank document
        except FileNotFoundError:
            self.datafile = open("patchdata.csv",'w')
            self.datafile.close()

        #make the Dfilelines and current data
        self.dfilelines = self.makeDfilelines()
        self.currentData = self.getCurrentData()

        #list of patches, from input
        self.patchList = []
        self.makePatchList()
        
        #number of patches user has on
        self.no_of_pat = len(self.patchList)

        #the email is located at the end of the patchdata file
        self.findEmail()

        #number of patches the user has used ever
        self.backlog_init()

        #get start date from backlog
        try:
            self.startdate = self.getStartDate()
        except IndexError:
            self.startdate = None

        #date of when changed first patch
        try:
            self.startdate = self.getStartDate()
        except IndexError:
            self.startdate = None

        #convert patches to readable format
        self.patches = self.getPatches()

        #optimizer attributes
        try:
            optfile = open("optfile.csv",'r')
            
        #if file not found, make blank one
        #start off Optimize is off
        except FileNotFoundError:
            optfile = open("optfile.csv",'w')
            optfile.write('0')
            optfile.close()
            optfile = open("optfile.csv",'r')
        if optfile.readline() == '1':
            self.optimized = True
        else:
            self.optimized = False
        optfile.close()

        #next patch change date/time
        #on start up, patchdata is empty, so it is yet to build..
        try:
            self.reminder = self.patchList[0].halfweek_plus()
        except IndexError:
            self.reminder = ''
        
    def __repr__(self):
        return self.patches

    def __str__(self):
        return self.patches

    def getOptiLoc(self):
        return self.optiLoc

    def getOptiLoR(self):
        return self.optiLoR

    def getReminder(self):
        return self.reminder

    def findEmail(self):
        #the email is located at the end of the patchdata file
        try:
            datafile = open("patchdata.csv",'r')
            dlines = datafile.readlines()
            check_line = dlines[-1]
            if '@' in check_line:
                self.email = check_line
            datafile.close()
        except IndexError:
            self.email = None

    def makeDfilelines(self):
        #make dfilelines by grabbing data
        #don't add email to dfilelines
        self.datafile = open('patchdata.csv','r')
        dflines = self.datafile.readlines()
        email = False
        for line in dflines:
            for ch in line:
                if ch == '@':
                    email = True
        if email == True:
            del dflines[-1]
        self.datafile.close()
        return dflines
    
    def getPatches(self):
        #makes a string object of the same patches
        patches = ''
        for patch in self.patchList:
            patches += str(patch)
            if patch != self.patchList[-1]:
                patches += ', '
        return patches

    def getStartDate(self):
        #find day of first patch change
        #make a data list on the first patch
        backlog = open("backlog.csv",'r')
        blogdata = backlog.readline()
        blogdata = blogdata.strip('\n')
        blogdata += ','
        bdisdata = []
        dat = ''
        for ch in blogdata:
            if ch == ',':
                bdisdata.append(dat)
                dat = ''
            else:
                dat += ch

        #the last two data pieces are the month and the day
        return bdisdata[5] + '-' + bdisdata[6]

    def makePatchList(self):
        for l in self.currentData:
            aPatch = Patch(l[0],l[1],l[2],l[3],l[4],l[5],l[6])
            self.patchList.append(aPatch)

    def switch_optimize(self):
        #remember optimize state
        optfile = open('optfile.csv','w')
        
        #switch optimize on or off
        if self.optimized == True:
            self.optimized = False
            optfile.write("0")
        else:
            self.optimized = True
            optfile.write("1")
        self.optiLoc = self.make_optiLoc
        self.optiLoR = self.make_optiLoR
        optfile.close()

    def useBacklogforOpti(self):
        #get necessary info from backlog to create optiLoc
        optiData = []
        try:
            ofile = open('backlog.csv','r')
            olines = ofile.readlines()[-4:]
            optiData = []
            for line in olines:
                optiData.append(line[:4])
                optiData.append(line[5:6])
        except IndexError:
            optiData = None
        return optiData
            
    def make_optiLoc(self):
        #this is for three patches
        #determines optimum location by picking the one with less patches
        if self.optimized == True:

            if self.no_of_pat % 2 != 0:
            #this version works only if you have an odd number of patches
                ldict = {'Stom':0,'Butt':0}
                for patch in self.patchList:
                    ldict[patch.getLocation()] += 1
                stomCount = ldict['Stom']
                buttCount = ldict['Butt']
                if stomCount > buttCount:
                    optiLoc = 'Butt'
                if stomCount < buttCount:
                    optiLoc = 'Stom'

            if self.no_of_pat % 2 == 0:
            #if even number, 'optimize' merely switches opposite attributes
                changePatch = self.patchList[0]
                if str(changePatch)[2] == 'S':
                    optiLoc = 'Butt'
                if str(changePatch)[2] == 'B':
                    optiLoc = 'Stom'
        else:
            optiLoc = None
        return optiLoc

    def make_optiLoR(self):
        #this is for three patches
        #determines optimum Left or Right by choosing less popular
        if self.optimized == True:
            
            if self.no_of_pat == 1 or self.no_of_pat == 3:            
            #this version works only if you have an odd number of patches
                ldict = {'L':0,'R':0}
                for patch in self.patchList:
                    ldict[patch.getLoR()] += 1
                elCount = ldict['L']
                arCount = ldict['R']
                if elCount > arCount:
                    optiLoR = 'R'
                if elCount < arCount:
                    optiLoR = 'L'

            if self.no_of_pat == 2 or self.no_of_pat == 4:
            #if even number, 'optimize' merely switches opposite attributes
                changePatch = self.patchList[0]
                if str(changePatch)[0] == 'L':
                    optiLoR = 'R'
                if str(changePatch)[0] == 'R':
                    optiLoR = 'L'
        else:
            optiLoR = None
        return optiLoR

    def makeNewPatch(self,LOC=None,LOR=None):
        now = datetime.datetime.now()
        date = datetime.date.today()
        
        #automatically sets time and day as current
        day = calendar.day_name[date.weekday()]
        time = str(now)[11:16]

        year = str(date)[:4]
        month = str(date)[5:7]
        dayN = str(date)[8:10]

        if self.optimized == True:
            loc = self.make_optiLoc()
            LoR = self.make_optiLoR()
        #these will be entered if Optimize is off
        else:
            loc = LOC
            LoR = LOR
        
        #replaces your oldest patch with a new one
        #loc and LoR are inputs of function that make the new Patch
        newPatch = Patch(loc,LoR,day,time,year,month,dayN)
        return newPatch
        
    def changePatch(self,newPatch):
        #delete old patch from list and replace it with new
        #self.patchList = [self.patchList[1], self.patchList[2],newPatch]
        self.patchList = self.patchList[1:]
        self.patchList.append(newPatch)

        #update patch string
        self.patches = self.getPatches()

        del self.dfilelines[0]

        #make new line from new patch for writing
        line = ''
        line += newPatch.location + ','
        line += newPatch.LoR + ','
        line += newPatch.day + ','
        line += newPatch.time + ','
        line += str(newPatch.year) + ','
        line += str(newPatch.month) + ','
        line += str(newPatch.dayN)
        line += '\n'

        #add the line we composed
        self.dfilelines.append(line)
        
        #open files for writing
        datafile = open("patchdata.csv",'w')
        copyfile = open("patchdata - Copy.csv",'w')
        backlog = open("backlog.csv",'a')

        #write files
        for line in self.dfilelines:
            datafile.write(line)
            copyfile.write(line)
        backlog.write(self.dfilelines[-1])
            
        datafile.close()
        copyfile.close()
        backlog.close()
        
        #re-establish current data and file
        self.currentData = self.getCurrentData()

        self.optiLoc = self.make_optiLoc()
        self.optiLoR = self.make_optiLoR()
        self.reminder = self.patchList[0].halfweek_plus()
        self.newPatch = self.makeNewPatch()

        #re init backlog
        self.backlog_init()

        #in case its first time, make the start date
        self.startdate = self.getStartDate()

        #remove email line (if there is one)
        #and than add email (if they requested)
        #removal of email line is because of dfilelines
        self.dfilelines = self.makeDfilelines()
        try:
            self.add_email()
        except AttributeError:
             None

    def backlog_init(self):
        #initialized backlog of data
        try:
            self.backlog = open("backlog.csv",'r')
            self.backloglines = self.backlog.readlines()
            self.no_pat_ever = len(self.backloglines)
            self.backlog.close()
        #if it doesnt already exist, create a new one
        except FileNotFoundError:
            self.backlog = open("backlog.csv",'w')
            self.backlog.close() 

    def change_email(self):
        #this should get rid of old email on dfilines
        self.dfilelines = self.makeDfilelines()
        #only called during change/add email part
        datafile = open("patchdata.csv",'w')
        #write lines
        for line in self.dfilelines:
            datafile.write(line)
            #add changed email
        datafile.write(self.email)
        datafile.close()
    
    def add_email(self):
        #happens in email trouble
        #adds email to data file for first time
        try:
            self.datafile = open("patchdata.csv",'a')
            self.datafile.write(self.email)
            self.datafile.close()
                      
        #if there is no email, nothing will happen
        except TypeError:
            return

    def remove_email(self):
        self.email = None
        newfile = open("patchdata.csv",'w')
        #since email is always the last line
        #copy all except last line.
        for line in self.dfilelines:
            newfile.write(line)
        newfile.close()
        
    def newPatchDis(self,newPatch):
        return ("Put your new patch here: " + str(self.makeNewPatch())[:6])

    def getCurrentData(self):               
    #gets info from current CSV for schedule init
    #returns list of patch data for schedule init
        pplist = []
        patchData = []
        for line in self.dfilelines:
            line = line.rstrip('\n')
            line += ','
            data = ''
            for ch in line:
                if ch == ',':
                    data = data.strip(',')
                    patchData.append(data)
                    data = ''     
                data += ch
                if len(patchData) == 7:
                    pplist.append(patchData)
                    patchData = []
        return pplist

    def emailSchedule(self):
        olMailItem = 0x0
        obj = win32com.client.Dispatch("Outlook.Application")
        newMail = obj.CreateItem(olMailItem)
        newMail.Subject = "Happy Patch Day"
        newMail.Body = str(self) + '\n' + self.getReminder()
        newMail.To = self.email

        #uncomment out if you wanna email the csv file as attachment
        #attachment1 = "pathname.csv"
        #newMail.Attachments.Add(Source=attachment1)
        
        newMail.display()
        newMail.Send()
