#Workout Generator 1.1
import random
import sys
import workout_arrays

class exercise:
    name=str()
    id=0
    modifier=str()
    reps=0

file="exercises.txt"
config=workout_arrays.loadSettings("config.txt")
if not config==False:
    file=config["read"]
    writing=bool(config["writing"])
    write=config["writeTo"]
    modDivider=config["modDivider"]
    modChance=config["modChance"]
else:
    print("Invalid configuration file.")
    input("Press enter to exit program.")
    sys.exit()
titles=()
exercises=()
difficulty={}
moddable=()
modIDs={}
modifiers=()
timed=()

#testing purposes
def numAllExercises():
    for n in range(0,len(exercises)):
        print("{} - {}".format(n,exercises[n]))

#makes a list of data based on dict specifications
def getInfo(dlist,spec):
    temp=[]
    rangeL=spec
    for n in range(0,int(len(rangeL)/2)):
        for x in range(rangeL[0+(n*2)],rangeL[1+(n*2)]+1):
            temp.append(dlist[x])
    return temp

#num is the chance of true being returned
def chance(num):
    if num == -1:
        return False
    temp=random.random()
    if temp>num:
        return False
    else:
        return True
        
#checks if generation command is valid
def genValid(var,titleArr,modArr):
    diff=("e","m","h")
    mod=("y","n")
    if titleArr.count(var[0])==0:
        return False
    if diff.count(var[1])==0:
        return False
    if var[2].isnumeric()==False or int(var[2])<2:
        return False
    if mod.count(var[3])==0:
        return False
    if var[3]=="y" and len(modArr)==0:
        print("Provided file has no modifiers!")
        return False
    return True

#set generator
def setGen(amt,diff):
    names=("e","m","h")
    setNum=1
    tempArr=["Error"]
    if diff=="e":
        tempArr=(str(amt-1)+"/e","1/e")
    elif amt<5:
        if amt==4:
            if diff=="h":
                tempArr=("1/e","1/m","2/h")
            if diff=="m":
                tempArr=("1/e","3/m")
        if amt==3:
            tempArr=("1/"+names[names.index(diff)-1],"2/"+diff)
        if amt==2:
            tempArr=("1/"+names[names.index(diff)-1],"1/"+diff)
        return tempArr
    elif diff=="m":
        setNum=amt-1
        tempArr=[str(amt-setNum)+"/e"] #cooldown
        setNum=(setNum//2)+1
        tempArr.insert(0,str(setNum)+"/m") #workingsets
        setNum=amt-1-setNum
        tempArr.insert(0,str(setNum)+"/e") #warmup
    else:
        setNum=amt-1
        tempArr=[str(amt-setNum)+"/e"] #cooldown
        setNum=(setNum//3)+1
        if float(setNum)==amt/3:
            setNum+=1
        tempArr.insert(0,str(setNum)+"/h") #workingsets
        tempNum=amt-1-setNum
        setNum=(amt-1-setNum)//2
        tempArr.insert(0,str(setNum)+"/m") #medsets
        setNum=tempNum-setNum
        tempArr.insert(0,str(setNum)+"/e") #warmup
    return tempArr

#repetition number generator
def genReps(diff):
    if chance(0.2):
        return "MAX"
    else:
        if diff=="e":
            a,b=15,25
        elif diff=="m":
            a,b=8,18
        else:
            a,b=5,10
        c=random.randint(a,b)
        if float(c//5)!=c/5 and c%2==1:
            c+=1
        return c

#modifier generator
def addMod(wtype,mList):
        availableMods=[]
        for x in range(0, len(wtype)):
            availableMods.append(mList[wtype[x]])
        mod=availableMods[random.randint(0,len(availableMods)-1)]
        temp=str(mod)
        return temp

def repsToSecs(repNum):
    time=int()
    if repNum=="MAX":
        return repNum
    if repNum>15:
        x=repNum/5
    else:
        x=repNum/4
    time=round(repNum*x)
    return time

data=workout_arrays.analyzeLines(file)
titles=tuple(data[0])
exercises=tuple(data[1])
moddable=tuple(data[2])
difficulty=dict(data[3])
modifiers=tuple(data[4])
modIDs=dict(data[5])
timed=tuple(data[6])
del data
while True:
    temp=input("Type your command. 'help' for help.\n")
    cmdGood=False
    if temp.find("help")!=-1:
        workout_arrays.helpMsg(temp)
    elif temp=="show":
        numAllExercises()
    elif temp.find("read")!=-1:
        tempArr=temp.split(" ")
        oldfile=str(file)
        file=tempArr[1]
        try:
            data=workout_arrays.analyzeLines(file)
            titles=tuple(data[0])
            exercises=tuple(data[1])
            moddable=tuple(data[2])
            difficulty=dict(data[3])
            modifiers=tuple(data[4])
            modIDs=dict(data[5])
            timed=tuple(data[6])
            del data
            tempArr.clear()
            print("File changed from '{}' to '{}'.".format(oldfile,file))
        except FileNotFoundError:
            print("File not found. Defaulting back to 'exercises.txt'.")
            file="exercises.txt"
        del oldfile
    elif temp.find("write")!=-1:
        if temp=="write n":
            writing=False
            print("Writing off.")
        elif temp=="write y":
            writing=True
            print("Writing on.")
        else:
            tempArr=temp.split(" ")
            write=tempArr[1]
            print("New workouts will be written to '{}'.".format(write))
    elif temp.find("exit")!=-1:
        sys.exit()
    elif temp.find("-")==-1:
        print("Invalid command. Try 'help'.")
    else:
        cmd=temp.split("-")
        if genValid(cmd,titles,modifiers)==False:
            print("Invalid command. Try 'help'.")
        else:
            cmdGood=True
            cmd[2]=int(cmd[2])
    while cmdGood:
        sets=tuple(setGen(cmd[2],cmd[1]))
        tempList=[]
        workout=[]
        tempEx=""
        oldID=-1
        if cmd[3]=="n":
            chanceflt=int(-1)
        else:
            chanceflt=modChance
        for a in range(0,len(sets)):
            instruction=sets[a].split("/")
            tempList=getInfo(exercises,difficulty[cmd[0]+"-"+instruction[1]])
            for b in range(0,int(instruction[0])):
                newEx=exercise()
                newEx.name=tempList[random.randint(0,len(tempList)-1)]
                newEx.id=exercises.index(newEx.name)
                if newEx.id==oldID:
                    tempList.remove(exercises[oldID])
                    newEx.name=tempList[random.randint(0,len(tempList)-1)]
                    newEx.id=exercises.index(newEx.name)
                    tempList.append(exercises[oldID])
                newEx.reps=genReps(instruction[1])
                if timed.count(newEx.id)==1:
                    newEx.reps=repsToSecs(newEx.reps)
                    newEx.reps="x"+str(newEx.reps)+" sec"
                else:
                    newEx.reps="x"+str(newEx.reps)
                if moddable.count(newEx.id)==1:
                    if chance(chanceflt):
                        chanceflt-=0.1
                        newEx.modifier=addMod(modIDs[cmd[0]],modifiers)
                    elif isinstance(chanceflt,float):
                        chanceflt+=0.1
                if newEx.modifier!="":
                    workout.append(newEx.modifier+modDivider+newEx.name+" "+str(newEx.reps))
                else:
                    workout.append(newEx.name+" "+str(newEx.reps))
                oldID=newEx.id
                del newEx
        if writing:
            for x in range(len(workout)):
                workout[x]=str(x+1)+".\t"+workout[x]+"\n"
            a=open(write,mode="w")
            a.write(cmd[0].upper()+" WORKOUT\n")
            a.writelines(workout)
            print("Wrote {} sets to '{}'.".format(len(workout),write))
            a.close()
        else:
            for c in range(len(workout)):
                print("{}.\t{}".format(c+1,workout[c]))
        cmdGood=False