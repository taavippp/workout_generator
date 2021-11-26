#Write line by line
#First char syntax: # for comment, ! for category, % for moddable exercise, = for timed exercise, ? for title
#Title (?) would be push OR pull, categories would then be push-e, push-m
#Mods are specified after title, example: ?push:wide grip,narrow grip,slow

def analyzeLines(file):
    a=open(file,mode="r")
    b=a.readlines()
    for n in range(len(b)):
        b[n]=b[n].rstrip("\n")
    fileRead=False
    x=0
    title=str()
    titles=[]
    exercises=[]
    moddable=[]
    ranges={}
    modifiers=[]
    modIDs={}
    timed=[]
    rangeStart=int(-1)
    rangeEnd=int(-1)
    while fileRead==False:
        if len(b[x])==0 or b[x][0]=="#":
            x=x+1
            continue
        if b[x][0]=="?":
            tempInfo=b[x].strip("?").split(":")
            titles.append(tempInfo[0])
            modifiers.extend(getMods(tempInfo[1],modifiers))
            modIDs.update({tempInfo[0]:getIDs(tempInfo[1],modifiers)})
            x=x+1
            continue
        if b[x][0]=="!":
            if len(ranges.values())==0 and rangeStart==-1:
                rangeStart=0
            else:
                rangeEnd=len(exercises)-1
                ranges.update({title:[rangeStart,rangeEnd]})
            title=b[x].strip("!")
            rangeStart=len(exercises)
            x=x+1
            continue
        if b[x].count("%")!=0:
            moddable.append(len(exercises))
        if b[x].count("=")!=0:
            timed.append(len(exercises))
        exercises.append(b[x].strip("%="))
        if x!=len(b)-1:
            x=x+1
        else:
            rangeEnd=len(exercises)
            ranges.update({title:[rangeStart,rangeEnd]})
            fileRead=True
    data=(titles,exercises,moddable,ranges,modifiers,modIDs,timed)
    a.close()
    if len(titles)==0 or len(exercises)==0 or len(titles)==0:
        return "{} is missing necessary data.".format(file)
    return data

def getMods(line,arr):
    a=list(line.split(","))
    for b in arr:
        if b in a:
            a.remove(b)
    return a

def getIDs(line,arr):
    ids=[]
    a=line.split(",")
    for b in a:
        ids.append(arr.index(b))
    return ids

def helpMsg(command):
    if command.strip("help")=="":
        print("TRY:\n\thelp-gen\n\thelp-read\n\thelp-write\n\texit\nInstructions are written according to the exercises.txt file.")
    elif command.replace("help-","")=="gen":
        print("TIPS ON GENERATING A WORKOUT\nWORKOUT/DIFFICULTY/SETS/MOD\nExample command: pull-h-10-y")
        print("WORKOUT:\n\tpush\n\tpull\n\tlegs\nThe kind of workout you wish to do.")
        print("DIFFICULTY:\n\te - easy\n\tm - medium\n\th - hard\nWhat difficulty your workout is going to ramp up to.")
        print("SETS:\n\tinteger\nYour number of sets. Minimum 2 sets.")
        print("MOD:\n\ty - yes\n\tn - no\nSome exercises can potentially get modifiers.")
    elif command.replace("help-","")=="read":
        print("TIPS ON USING YOUR OWN EXERCISE LIST")
        print("By default, the program uses exercises.txt included with the program.")
        print("Instructions on changing the list itself can be found on the first lines of the file.")
        print("You can specify a new list to use in the program.\nExample command: read yourfilename.txt")
    elif command.replace("help-","")=="write":
        print("TIPS ON WRITING YOUR WORKOUT TO A FILE")
        print("By default, your workout WILL be written to 'workout.txt'.")
        print("You can toggle writing with following commands:\n\twrite n\n\twrite y")
        print("You can specify a new file to write to with following example command:\n\twrite newfile.txt")
    else:
        print("Invalid help command. Try simply 'help'.")

def loadSettings(file):
    a=open(file,mode="r")
    b=a.readlines()
    for n in range(len(b)):
        b[n]=b[n].rstrip("\n")
    fileRead=False
    c=0
    data={}
    while fileRead==False:
        temp=b[c].split(":")
        if temp[1][len(temp[1])-1].isdigit():
            if temp[1].isdigit():
                temp[1]=int(temp[1])
            else:
                temp[1]=float(temp[1])
        data.update({temp[0]:temp[1]})
        if c==len(b)-1:
            fileRead=True
        c=c+1
    keys=list(data.keys())
    try:
        if keys.index("read")>=0 and keys.index("writing")>=0 and keys.index("modDivider")>=0 and keys.index("modChance")>=0:
            if bool(int(data["writing"]))==True and not keys.count("writeTo"):
                return False
            del keys
    except ValueError:
        return False
    return(data)