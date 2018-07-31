from patches import *
from tkinter import *
from tkinter.font import Font
from random import *
from tkinter import filedialog

# PatchDay HRT Software
# by Juliya Smith
# 2016

# PatchDay Strings
pdStrs = ["Have you changed it?",
       "You could always add your email later.",
       "Would you not like me to ask again?",
       "Would you like to enter one?",
       "You don't have an email on file.",
       "Okay, I won't ask again...",
       "Fine then :)",
       "Schedule emailed!",
       "Current Patches: ",
       "Enter your email at the bottom.",
       "Click 'Enter' to upload patch data...",
       "Click 'Finish' when you're done entering all your current patch data and are ready to move on...",
       "Email saved into system! PatchDay is ready to use.",
       "Welcome to PatchDay!  PatchDay is a schedule optimizer for medicinal patches.  Please see README!",
       "Patch Updated!",
       "Enter patch data to intitiate PatchDay scheduling: ",
       "(part of body, left side or right side" + '\n' + "day of week, year, month num, day num)",
       "[Follow this rubric (including commas)]: ",
       "Stom,L,Sunday,12:35,2016,8,28",
       "Entry added!",
       "Done entering . . . PatchDay is now usable. " +
          "Click 'NotPatchDay' to see schedule and get a reminder. " +
          "Click 'PatchDay' to automatically update your patch. " +
          "(you won't have to enter hard-data ever again!)",
       "Click 'Save' to upload your email...",
       "**************************",
       "Entry is not good!  Check your formatting!",
       "Are you sure you want to create a new schedule?" + '\n' +
          "This will erase your previous patch data.",
       "You're schedule has been cleared...",
       "Optimize mode optimizes the location to put your next patch." + '\n'
          "Would you like to turn 'on' Optimize?",
       "Optimize is now on!",
       "Optimize is now off!",
       "Optimize mode optimizes the location to put your next patch." + '\n'
          "Would you like to turn 'off' Optimize?",
       "Would you like to remove your email from Patch Day?",
       "Email removed!",
       "It's okay, there is no email on record.",
       "Not enough backlog to turn on optimize yet." + '\n'
          "Continuing using PatchDay and and you will soon have this feature.",
       "Optimize mode is a key feature of PatchDay," + '\n'
          "It will determine the optimal places to put your next patch," + '\n'
          "The Optimize feature activates a one-click patch change system." + '\n'
          "Otherwise, you just have to enter some data manually each time.",
       "Where did you place your new patch?(L/R)(Stom/Butt)" + '\n' +
          "Enter in the following format: ",
       "Stom,L",
       "No changes made to the Optimization feature.",
       "This is the number of patches you have changed with PatchDay...",
       "Are you sure you want to permanently delete your history of patches?",
       "Backlog has been cleared."
        ]

welcomeStrs = [
       "'Is it..?' or 'is it not..?' Patch Day..." + '\n'
          "That's my question...",
       "Welcome friend ... is it Patch Day?",
       "So is it patch day today or what? What's up?",
       "Welcome to your favorite patch medication software!!! Woot!!!",
       "How many ways can we say PATCH DAY!!!",
       "It's more than just 'Patch Day'... its whatever you make it!",
       "If it's Patch Day and you know it, click some buttons..." + '\n'
         "If it's Patch Day and you know it, click some buttons..." + '\n'
         "... Okay, I'll stop ...",
       "Gooooooood Morniiiing PATCHDAY!!!"
          ]


mypink = "#ffe6ff"
myblack = "#000000"

#this is the front-end for PatchDay!

class Application(Frame):

    def createWidgets(self):

        #menubar
        self.menubar = Menu(root, background='#000099',
        foreground='white', activebackground='#004c99',
        activeforeground='white')
        root.config(menu=self.menubar)

        #file menu
        self.filemenu = Menu(self.menubar, tearoff=0,
        background='#ffe6ff',
        foreground='black', activebackground='#99e699',
        activeforeground='black')
        self.filemenu.add_command(label="New Schedule",
        command=self.newSchedule_prompt)
        self.filemenu.add_command(label="Make a Copy",
        command=self.savenewfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Change/Add Email",
        command=self.changeEmail_prompt)
        self.filemenu.add_command(label="Remove Email",
        command=self.removeEmail_prompt)
        try:
            if type(self.s.email) != str:
                self.filemenu.entryconfig("Remove Email", state="disabled")
        except AttributeError:
            self.filemenu.entryconfig("Remove Email", state="disabled")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Display Count",
        command=self.backlog_count)
        self.filemenu.add_command(label="Clear Backlog",
        command=self.clearBacklog_prompt)
        if type(self.s.startdate) != str:
            self.filemenu.entryconfig("Display Count", state="disabled")
            self.filemenu.entryconfig("Clear Backlog", state="disabled")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        #switches menu
        self.switchesmenu = Menu(self.menubar,
        tearoff=0, background='#ffe6ff',
        foreground='black', activebackground='#99e699',
        activeforeground='black')
        #determine if optimize of on or off for display
        olab = self.optipowerOlab()
        self.optipowerDis(olab)
        self.menubar.add_cascade(label="Switches",
        menu=self.switchesmenu)
        self.switchesmenu.add_separator()
        #background data grab
        self.switchBackgroundMenu()
        
        #patch buttons
        self.npdB = Button(self)
        self.pdB = Button(self)
        self.npdB.grid(row=0,column=0)
        self.pdB.grid(row=1,column=0)

        #text display area
        self.ptext = 0
        self.makePtext()

        #text tags
        self.ptext.tag_add('important', END)
        self.ptext.tag_configure('important',background='light yellow',
        font='helvetica 10 italic', relief='raised')
        self.pdB["text"] = "Patch Day"
        self.npdB["text"] = "Not Patch Day"
        
        #add the scrool bar and connect it with self.ptext
        scrollb = Scrollbar(self, command=self.ptext.yview)
        scrollb.grid(row=3, column=1, sticky='nsew')
        self.ptext['yscrollcommand'] = scrollb.set
        self.ptext.see(END)

        self.vsb = Scrollbar(self, orient="vertical",
        command=self.ptext.yview)

        #user 'yes' or 'no' controls
        self.yes = Button(self)
        self.no = Button(self)
        self.disYesnNo()

        #for entering data, like email
        self.entry = Entry(self,width=45)
        self.entry.grid(row=6,column=0)

    def switchBackgroundMenu(self):
        bg = self.readBackgroundColor()
        
        self.switchesmenu.add_command(label="Change Theme",
            command=self.changeBackground)

    def changeBackground(self):
        bg = self.readBackgroundColor();
        bgdata = open('backgroundcolor.csv','w')
        if bg == myblack:
            bgdata.write(mypink)
        else:
            bgdata.write(myblack)
        bgdata.close()
        self.patchAppStart()
        i = randint(0,7)
        app.disText(welcomeStrs[i],sB=False) 

    def disText(self, text,sB=True,sA=True):
        #boolean for displaying space before
        if sB == True:
            self.ptext.insert(END, '\n')

        self.ptext.insert(END, text)
        
        #boolean for displaying space after
        if sA == True:
            self.ptext.insert(END, '\n')

        #go to current/bottom of display self.ptext as it grows
        self.ptext.see(END)
        
    def disPatches(self):
        for patch in self.s.patchList:
            self.disText(str(patch),sB=False)

    def disExText(self,i):
        self.ptext.insert(END,'\n')        #tag for important text
        self.ptext.insert(END, pdStrs[i], ("important"))
        self.ptext.insert(END,'\n')
        
    def patchAppStart(self):
        #activates the main Patch Day application
        #by making the buttons active
        self.pdB["state"] = ACTIVE
        self.npdB["state"] = ACTIVE

        #also activates file menu
        self.menubar.entryconfig("File", state="active")
        
        self.npdB["command"] = self.notPatchDay
        self.pdB["command"] = self.patchDay

        self.yes["text"] = 'Yes'
        self.no["text"] = 'No'

        self.yes["state"] = DISABLED
        self.no["state"] = DISABLED

        self.entry["state"] = DISABLED

        self.makePtext()

        #on conditions where these are left DISABLED
        self.filemenu.entryconfig("Change/Add Email", state="normal")
        self.filemenu.entryconfig("Display Count", state="normal")
        self.filemenu.entryconfig("Clear Backlog", state="normal")

    def disYesnNo(self):
        #display "yes" and "no" buttons,
        #prepared for being asked about if you changed
        #your patch or not...
        self.yes.grid(row=4,column=0)
        self.no.grid(row=5,column=0)
        
        self.yes["text"] = "Yes"
        self.no["text"] = "No"

    def determine_ready(self):
        if self.s.currentData == []:
            self.ready = False
        else:
            self.ready = True

    def getUserPref(self):
        #user pref is for not asking for email again if user doesnt want
        try:
            userpref = open("userpref.csv",'r')
            #if its empty file
            try:
                userpreflines = userpref.readlines()
                up = userpreflines[0]
                return up
            except IndexError:
                return None
        except FileNotFoundError:
            return None

    def readBackgroundColor(self):
        try:
            backgroundcolor = open("backgroundcolor.csv",'r')
            #if its empty file
            try:
                bglines =backgroundcolor.readlines()
                bg = bglines[0]
                return bg
            except IndexError:
                return None
        except FileNotFoundError:
            return None

    def makePtext(self):
        bgC = self.readBackgroundColor()
        if bgC == "#000000":
            fg = "#FFFFFF"
        else:
            fg = "#000000"
        self.ptext = Text(self,width=70,height=15,bg=bgC,
        undo=True,wrap='word',foreground=fg)
        self.ptext.grid(row=3,column=0)

    def start_up(self):
        self.pdB["state"] = DISABLED
        self.npdB["state"] = DISABLED
        self.filemenu.entryconfig("Change/Add Email", state="disabled")
        self.filemenu.entryconfig("Remove Email", state="disabled")
        self.filemenu.entryconfig("Make a Copy", state="disabled")
        self.filemenu.entryconfig("Display Count", state="disabled")
        self.filemenu.entryconfig("Clear Backlog", state="disabled")
        
        self.yes["text"] = 'Enter'
        self.no["text"] = 'Finish'

        self.disText(pdStrs[13],sB=False)
        self.disText(pdStrs[15],sA=False)
        self.disText(pdStrs[17])
        self.disExText(18)
        self.disText(pdStrs[16])
        self.disText(pdStrs[10])
        self.disText(pdStrs[11],sB=False)

        self.yes["command"] = self.grabEntr
        
        self.no["state"] = DISABLED

        #for enter button to work
        self.no["command"] = self.done_entering

        self.entry["state"] = NORMAL

    def newSchedule_prompt(self):
        self.disText(pdStrs[25])
        self.no["state"] = ACTIVE
        self.yes["state"] = ACTIVE
        self.no["text"] = 'No'
        self.yes["text"] = 'Yes'
        self.yes["command"] = self.newSchedule
        
        self.no["command"] = self.ans_noAsA

    def changeEmail_prompt(self):
        #happens when click add/change email at the top
        self.disText(pdStrs[9])
        self.disText(pdStrs[22])
        self.yes["text"] = 'Save'
        self.yes["command"] = self.changeEmail
        
        self.yes["state"] = ACTIVE
        self.entry["state"] = NORMAL

    def changeEmail(self):
        #grabs entered email
        self.s.email = self.entry.get()

        #if statement checks formatting of entry
        if self.checkEmail(self.s.email):

            #appends email to datafile
            self.s.change_email()

            #refresh entry text
            self.disText(pdStrs[23])
            self.disText(pdStrs[12])
            self.entry.delete(0, 'end')
            self.entry["state"] = DISABLED
            self.yes["state"] = DISABLED
            self.no["state"] = DISABLED

            self.filemenu.entryconfig("Change/Add Email", state="normal")
            self.filemenu.entryconfig("Remove Email", state="normal")

    def optimize_mode_prompt1(self):
        #happens in after start up and email trouble
        #for asking user if they want an optimized schedule
        self.disText(pdStrs[35])
        self.optimize_mode_prompt()

        #create to a file to remember asking this prompt
        remember = open('askdopti.csv','w')
        remember.write('1')
        remember.close()

    def optimize_mode_prompt(self):
        #happens from hitting 'Optimize' in switches drop down menu
        #offers you to turn optimize mode on
        if self.s.optimized == True:
            self.disText(pdStrs[30])
        else:
            self.disText(pdStrs[27])
        self.disText(pdStrs[23])
        
        self.yes["text"] = 'Yes'
        self.yes["command"] = self.toggleOptimize
        
        self.yes["state"] = ACTIVE
        self.no["text"] = 'No'
        self.no["command"] = self.ans_noOm
        self.no["state"] = ACTIVE
        self.entry["state"] = DISABLED
        self.pdB["state"] = DISABLED
        self.npdB["state"] = DISABLED

    def locnlor_entry_prompt(self):
        self.disText(pdStrs[36])
        self.disExText(37)
        self.disText(pdStrs[10])
        
        self.entry['state'] = NORMAL
        self.yes['state'] = ACTIVE
        self.no['state'] = DISABLED
        self.yes['text'] = 'Enter'
        self.yes['command'] = self.grab_locnlor_entry

        self.pdB['state'] = DISABLED
        self.npdB['state'] = DISABLED 

    def removeEmail_prompt(self):
        #happens when you clikc "Remove Email"
        self.disText(pdStrs[31])
        self.yes["state"] = ACTIVE
        self.no["state"] = ACTIVE
        self.yes["text"] = 'Yes'
        self.no["text"] = 'No'
        self.yes["command"] = self.removeEmail
        self.no["command"] = self.patchAppStart
        self.s.remove_email()

        #disable menubar 'remove email'
        self.filemenu.entryconfig("Remove Email", state="disabled")

    def clearBacklog_prompt(self):
        #happens when you click "Clear Backlog"
        self.disText(pdStrs[40])
        self.yes["state"] = ACTIVE
        self.no["state"] = ACTIVE
        self.yes["text"] = 'Yes'
        self.no["text"] = 'No'
        self.yes["command"] = self.clearBacklog
        self.no["command"] = self.ans_noCbl

    def clearBacklog(self):
        #writes an empty file in place of backlog
        backlog = open('backlog.csv','w')
        backlog.close()
        self.disText(pdStrs[41])
        self.s.backlog_init()

        self.patchAppStart()
    
    def finishlocnlor(self):
        return self.optiEntry   

    def toggleOptimize(self):
        self.s.switch_optimize()
        if self.s.optimized == True:
            self.disText(pdStrs[28])
        if self.s.optimized == False:
            self.disText(pdStrs[29])
            self.patchAppStart()
        olab = self.optipowerOlab()
        self.patchAppStart()

        #toggle menu label
        self.switchesmenu.entryconfig(1,label="Optimize" +
        ' -- ' + '(' + olab + ')',
        command=self.optimize_mode_prompt)

    def optipowerOlab(self):
        if self.s.optimized == True:
            olab = "is on"
        else:
            olab = "is off"
        return olab

    def optipowerDis(self,olab):
        #it takes the words 'On' or 'Off' for menu display
        self.switchesmenu.add_command(label="Optimize" +
        ' -- ' + '(' + olab + ')',
        command=self.optimize_mode_prompt)
        
    def newSchedule(self):
        self.disText(pdStrs[23])
        #creates an empty datafile to replace old one
        self.disText(pdStrs[26])
        file = open('patchdata.csv','w')
        file.close()

        #creates an empy userpref to erase old email preferences
        ufile = open('userpref.csv','w')
        ufile.close()

        #begin refill by restarting application        
        self.start_up()

    def email_trouble(self):
        #if there is not email on file, this runs
        #it asks if you would to enter one
        self.disText(pdStrs[4])
        self.disText(pdStrs[3],sB=False)

        self.yes["text"] = 'Yes'
        self.no["text"] = 'No'
        self.yes["command"] = self.ans_yesEmF
        
        
        self.no["command"] = self.ans_noEmF
        self.yes["state"] = ACTIVE
        self.no["state"] = ACTIVE

        self.pdB["state"] = DISABLED
        self.npdB["state"] = DISABLED
        self.entry["state"] = DISABLED

    def grabEntr(self):
        entry = self.entry.get()
        
        #if statement checks formatting of entry
        if self.checkEntry(entry):

            #adds entry to datafile
            file = open("patchdata.csv",'a')
            file.write(entry + '\n')

            self.disText(pdStrs[19])
            self.disText(entry)

            #turn other button on after first entry entered
            #this is used to stop entering data
            self.no["state"] = ACTIVE

        #self.checkEntry is a series of queries
        else:
            self.disText(pdStrs[24])

        #refresh entry text
        self.entry.delete(0, 'end')

        #normalize some entry menu options
        self.filemenu.entryconfig("Make a Copy", state="normal")
        self.filemenu.entryconfig("Display Count", state="normal")
        self.filemenu.entryconfig("Clear Backlog", state="normal")
   
    def grabEmail(self):
        #grabs entered email
        self.s.email = self.entry.get()

        #if statement checks formatting of entry
        if self.checkEmail(self.s.email):

            #appends email to datafile
            self.s.add_email()

            #refresh entry text
            self.entry.delete(0, 'end')
            
            self.disText(pdStrs[12])
            self.disText(pdStrs[23])
            self.entry["state"] = DISABLED
            self.yes["state"] = DISABLED
            self.no["state"] = DISABLED

            self.filemenu.entryconfig("Change/Add Email", state="normal")
            self.filemenu.entryconfig("Remove Email", state="normal")            

            #now tell them about optimize mode
            if self.s.optimized == False:
                self.checkprev_optiprompt()
            else:
                self.patchAppStart()

        #if there is no '@' sign, it gets mad
        else:
            self.disText(pdStrs[24])
            self.entry.delete(0, 'end')

        #refresh entry text
        self.entry.delete(0, 'end')

    def grab_locnlor_entry(self):
        #make the optiEntry
        self.optiEntry = self.entry.get()
        self.entry.delete(0, 'end')
        if self.checkEntry_locnlor(self.optiEntry):
            self.changePatchUnOp()
            self.disText(pdStrs[19])
            self.patchAppStart()
        else:
            self.disText(pdStrs[24])
            self.locnlor_entry_prompt()

        #convenient time to email
        if type(self.s.email) == str:
            self.emailsend()
        
    def checkprev_optiprompt(self):
        #if file doesnt exist, give them the prompt
        #the existance of the file is proof
        try:
            remember = open("askdopti.csv",'r')
            remember.close()
            self.patchAppStart()
        except:
            self.optimize_mode_prompt1()            

    def checkEntry(self,entry):
        #get the data from the entry
        #use commas as referenec points
        #add comma at end for ease of query
        entry += ','
        entrydata = []
        data = ''
        for ch in entry:
            if ch == ',':
                entrydata.append(data)
                data = ''
            elif ch != ',':
                data += ch
            #should else only if its the last data..        
        #check that all parts of entry make sense.
        try:
            if entrydata[0] not in ['Stom','Butt']:
                return False
            if entrydata[1] not in ['L','R']:
                return False
            days = ['Sunday','Monday','Tuesday','Wednesday',
                    'Thursday','Friday','Saturday']
            if entrydata[2] not in days:
                return False
            try:
                x = int(entrydata[3][:2])
                x = int(entrydata[3][3:5])
            except ValueError:
                return False
            if entrydata[3][2] != ':':
                return False
            try:
                x = int(entrydata[4])
            except ValueError:
                return False
            try:
                x = int(entrydata[5])
            except ValueError:
                return False
            try:
                x = int(entrydata[6])
            except ValueError:
                return False

        except IndexError:
            return False
            
        return True

    def checkEntry_locnlor(self,entry):
        location = entry[:4]
        if location not in ['Butt','Stom']:
            return False
        lor = entry[5]
        if lor not in ['L','R']:
            return False
        return True

    def checkEmail(self,email):
        if '@' in email:
            return True
        else:
            return False

    def removeEmail(self):
        self.s.remove_email
        self.disText(pdStrs[32])
        self.patchAppStart()
    
    def done_entering(self):
        #update patch attributes
        self.s = Psched()
        
        self.entry["state"] = DISABLED
        self.yes["state"] = DISABLED
        self.no["state"] = DISABLED

        #move on
        self.ready = self.determine_ready()
        self.disText(pdStrs[23])
        self.disText(pdStrs[20])
        self.disText(pdStrs[23])
        self.email_trouble()

    def savenewfile(self):
        #opens save dialogue with windows

        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt', '.csv')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'patchdata.txt'
        options['parent'] = root
        options['title'] = 'Making a copy of patchdata'

        file = filedialog.asksaveasfile('w',**options)
        for patch in self.s.patchList:
            file.write(str(patch) +'\n')
        file.close()

    def ans_noEmF(self):
        #no, you don't want to enter email
        #but do you want to remove this question for next time?
        self.disText(pdStrs[2],sA=False)
        self.disText(pdStrs[1])
        self.yes["command"] = self.ans_yesAsA
        
        self.no["command"] = self.ans_noAsA

    def ans_yesEmF(self):
        #yes you want to enter an email during start up
        self.disText(pdStrs[9])
        self.disText(pdStrs[22])
        self.yes["text"] = "Save"
        self.yes["command"] = self.grabEmail
        self.yes["state"] = ACTIVE
        self.no["state"] = DISABLED
        self.entry["state"] = NORMAL
        
    def ans_noAsA(self):
        #no, don't remove email question for next time.
        self.disText(pdStrs[6])

        self.yes["state"] = DISABLED
        self.no["state"] = DISABLED

        #now tell them about optimize mode
        if self.s.optimized == False:
            self.checkprev_optiprompt()
        else:
            self.patchAppStart()
            
    def ans_yesAsA(self):
        #creates extradata for remembering user preferences
        #won't ask for email again
        userpref = open("userpref.csv",'w')
        userpref.write("e:no")
        userpref.close()
        self.disText(pdStrs[6])

        self.yes["state"] = DISABLED
        self.no["state"] = DISABLED

        #now tell them about optimize mode
        if self.s.optimized == False:
            self.checkprev_optiprompt()
        else:
            self.patchAppStart()
        
    def ans_noPaD(self):
        #you answer no, you have not changed your patches
        self.disText(pdStrs[8])
        self.disPatches()
        self.disText(self.s.getReminder())

        self.yes['text'] = 'Yes'
        self.no['text'] = 'No'

        #for optimize mode, display where to put the new patch
        if self.s.optimized == True:
            self.disText(self.s.newPatchDis(self.s.makeNewPatch()))
        self.disText(pdStrs[0])

    def ans_yesPaD(self):
        #you answer yes, you have changed your patches
        if self.s.optimized == True:
            self.changePatch()

            #email results if they choose
            try:
                if type(self.s.email) == str:
                    self.emailsend()
            except AttributeError:
                None

        #updates patches the user-entry method
        if self.s.optimized == False:
            self.locnlor_entry_prompt()

    def ans_noOm(self):
        self.disText(pdStrs[38])
        self.patchAppStart()

    def ans_noCbl(self):
        self.disText(pdStrs[6])
        self.patchAppStart()

    def emailsend(self):
        if type(self.s.email) == str:
            self.s.emailSchedule()
            self.disText(pdStrs[7])

    def backlog_count(self):
        #display the count in the backlog
        #display the start date of the first patch
        self.disText(pdStrs[23])
        self.disText(pdStrs[39])
        
        # of only 1 patch changed, omit the 'es' on patches
        if self.s.no_pat_ever > 1:
            self.disText('\n' + str(self.s.no_pat_ever) +
            ' patches changed since ' + self.s.startdate + '.')
        elif self.s.no_pat_ever == 1:
            self.disText('\n' + str(self.s.no_pat_ever) +
            ' patch changed since ' + (self.s.startdate + '.'))
        else:
            self.disText('0')

        self.patchAppStart()

    def changePatchUnOp(self):
        #user entry for loc and lor
        location = self.optiEntry[:4]
        lor = self.optiEntry[5]

        newPatch = self.s.makeNewPatch(LOC=location,LOR=lor)

       #change the patch and update app  
        self.s.changePatch(newPatch)
        self.disText(pdStrs[14])
        self.disText(pdStrs[8])
        self.disPatches()

        self.yes["state"] = DISABLED
        self.no["state"] = DISABLED

    def changePatch(self):
        #make the new patch from patches.py        
        newPatch = self.s.makeNewPatch()

        #change the patch and update app  
        self.s.changePatch(newPatch)
        self.disText(pdStrs[14])
        self.disText(pdStrs[8])
        self.disPatches()

        self.yes["state"] = DISABLED
        self.no["state"] = DISABLED

    def notPatchDay(self):
        
        #for the Not Patch Day button!
        #...an extra space before the display
        self.yes["state"] = DISABLED
        self.no["state"] = DISABLED
        if self.patchDis == False:
            self.disText(pdStrs[8])

            self.disPatches()
            
            #if Optimize mode is on, tell user where to place next patch
            if self.s.optimized == True:
                self.disText(self.s.getReminder())             
                self.disText(self.s.newPatchDis(self.s.makeNewPatch()))

            self.patchDis = True
        
    def patchDay(self):        
        
        #for the Patch Day button!
        self.disText(self.s.getReminder())

        #if Optimize mode is on, tell user where to place next patch
        if self.s.optimized == True:
            self.disText(self.s.newPatchDis(self.s.makeNewPatch()),sB=False)

        self.disText(pdStrs[0],sB=False)
        
        #make yes and no buttons appropriate
        self.yes["command"] = self.ans_yesPaD 
        self.no["command"] = self.ans_noPaD      
        self.yes["state"] = ACTIVE
        self.no["state"] = ACTIVE
        self.yes['text'] = 'Yes'
        self.no['text'] = 'No'
        
    def __init__(self,master=None,background='light pink'):
        self.s = Psched()
        self.patchDis = False

        Frame.__init__(self, master,width=800,height=400)
        self.pack()
        self.createWidgets()

        self.img = Image("photo", file="icon.gif")
        root.tk.call('wm','iconphoto',root._w,self.img)

        #variable for letting you know app has run before
        self.ready = self.determine_ready()


root = Tk()
root.wm_title("PatchDay")
app = Application(master=root)
#first time starting up, we have to build database
app.determine_ready()
if app.ready == False:
    app.start_up()
    
#this loop runs if there is no email and the program has finished start_up()
else:
    try:
        if type(app.s.email) != str and app.getUserPref() == None:
            i = randint(0,7)
            app.disText(welcomeStrs[i],sB=False)
            app.email_trouble()
    except AttributeError:
            if app.getUserPref() == None:
                i = randint(0,7)
                app.disText(welcomeStrs[i],sB=False)
                app.email_trouble()

#this is the main display loop
try:
    if app.getUserPref() == "e:no" or type(app.s.email) == str:
        app.patchAppStart()
        i = randint(0,7)
        app.disText(welcomeStrs[i],sB=False)
except AttributeError:
    if app.getUserPref() == "e:no":
        app.patchAppStart()
        i = randint(0,7)
        app.disText(welcomeStrs[i],sB=False)        
app.mainloop()
