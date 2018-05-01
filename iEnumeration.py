
"""

@author: Guillermo Flores
e-mail: gflores10.1926@gmail.com
"""
''' ------------------------------------------EXAMPLE  1------------------------------------'''
'''
rD = {} #Empty dictionary where we will store restrictions (restrictions Dictionary)
rD [1]= ['a','e']
rD [2] = ['b','c']
rD [3] = ['c','d']
rD [4] = ['e','d']
rD [5] = ['a','b','d']
rD [6] = ['b','h','i']
rD [7] = ['a','h','i']
rD [8] = ['d','f','i']
rD [9] = ['f','g','h']
rD [10] = ['d','h','i']
#We could read user imputed values in a while loop and store them in the    
#    dictionary.
totVar = 9 #ammount of variables
totRestric = 10 #ammount of bilateral relations between variables
totRooms = 2 #ammount of available rooms
ren, col = totVar + 1, totVar
cost = [[0 for x in range(col)] for y in range (ren)]
var = {}
var ['a'] = []
var ['b'] = []
var ['c'] = []
var ['d'] = []
var ['e'] = []
var ['f'] = []
var ['g'] = []
var ['h'] = []
var ['i'] = []

#Start conditions, group restrictions
sC = {}
sC ['a'] = 3
sC ['b'] = 2
'''
'''------------------------END OF EXAMPLE 1 ---------------------------------'''

'''----------------------- EXAMPLE 2 ----------------------------------------'''

#List of needed variables
rD = {} #restrictions Dictionary
rD [1] = ['i','g']
rD [2] = ['a','c','e','g']
rD [3] = ['b','a','g']
rD [4] = ['e','g']
rD [5] = ['i','d','j','k']
rD [6] = ['m','i','d']
rD [7] = ['f','d','k']
rD [8] = ['a','f','l','k']
rD [9] = ['b','m']
rD [10] = ['g','k']
rD [11] = ['a','k','l','i']
rD [12] = ['a','h','l']
rD [13] = ['c','n','h','m']
rD [14] = ['c','b']
rD [15] = ['j','h']
var = {} #relations of letter Dictionary
var['a'] = []
var['b'] = []
var['c'] = []
var['d'] = []
var['e'] = []
var['f'] = []
var['g'] = []
var['h'] = []
var['i'] = []
var['j'] = []
var['k'] = []
var['l'] = []
var['m'] = []
var['n'] = []
sC = {} #start conditions Dictionary
sC['a'] = 3
sC['c'] = 3
sC['d'] = 3
sC['i'] = 4
totVar = 14 #ammount of variables
totRestric = 15 #ammount of bilateral relations between variables
totRooms = 2 #ammount of available rooms
ren, col = totVar + 1, totVar
cost = [[0 for x in range(col)] for y in range (ren)]
         

'''-----------------------END OF EXAMPLE 2 -----------------------------------'''
#get relations of every course
def relations(): 
    for i in range (0, len(var)) : #for every variable
        for j in range (1, totRestric+1) : #try every restriction 
            if chr(97+i) in set(rD[j]) :
                #in ASCII code from #97 starts the ABC
                var[chr(97+i)] = set(var[chr(97+i)]).union(set(rD[j])) - set(chr(97+i)) 
            #end if
        #end for
    #end  for
#end relations

#Get the number of relations each letter has, and fill the first row of the cost_matrix
def fillCosts():
    for i in range (0, len(var)) :
        cost[0][i] = len(set(var[chr(97+i)]))
    #end for
#end fill_costs

groups = {} #Hashtable with final groups and elements
group_restrictions = {} #Hashtable with restrictions to each 

#Adds element to certain group
def addToGroup(group, element):
    groups.setdefault(group,[])
    groups[group].append(element)
#end of addToGroup

#startConditions is a hashtable that stores the initial conditions of group allowance 
#it has as 'key' the letter and as 'value' the group it can belong to 
def addInitialRestrictions(startConditions): 
    for i in range (0, len(startConditions)):
        for j in range(0, startConditions[list(startConditions.keys())[i]]-1):
            group_restrictions.setdefault(list(startConditions)[i],[])
            group_restrictions[list(startConditions)[i]].append(j+1) 
#end addInitialRestrictions

#Receives the group not allowed and the list of letters that can't belong to the group
def addRestrictions(group, relations):
    for i in range (0, len(relations)):
        group_restrictions.setdefault(list(relations)[i],[])
        if group not in group_restrictions[list(relations)[i]]:
            group_restrictions[list(relations)[i]].append(group) 
    #end for
#end  addRestrictions

def decreaseRelatedColumns(row, maxValueIndex):
    cost[row+1][:] = cost[row][:] 
    for i in range (0, len(var[chr(97+maxValueIndex)])): 
        if(cost[row][ord(list(var[chr(97+maxValueIndex)])[i])-97] != -1):
            cost[row+1][ord(list(var[chr(97+maxValueIndex)])[i])-97] = cost[row][ord(list(var[chr(97+maxValueIndex)])[i])-97] - 1
    cost[row+1][maxValueIndex] = -1
    #end for
#end decreaseRelatedColumns    

def allAssigned(actualRow):
    assigned = 0 #boolean variable
    count = 0
    for i in range(0, totVar): 
        if cost[actualRow][i] == -1:
            count+=1
    if count == totVar:
        assigned = 1
    return assigned
#end allAssigned

def zeroIndex(actualRow):
    zeroIndex = -1
    for i in range(0, totVar):
        if not cost[actualRow][i]:
            zeroIndex = i
            break #We just found the zero index
    return zeroIndex
#end zeroIndex

def removeDuplicates(dictionary):
    result = {}
    for key,value in dictionary.items():
        if value not in result.values():
            result[key] = value
    return result
#end removeDuplicates

#get the group where I will store the letter 
def nextGroupToFill(indexToGroup):
    bestOption = 1
    letter = chr(97+indexToGroup)
    if len(groups) == 0: #We have no groups
        if letter in group_restrictions.keys(): #We've got some restrictions
            if bestOption not in group_restrictions[letter]:
                return bestOption
            else: 
                while(bestOption in group_restrictions[letter]):
                    groups[bestOption] = []
                    bestOption += 1
        else:
            return bestOption
    else:#We've created at least 1 group
        timeTablesWspace = {}
        count = 0
        #store all timetables with space
        for i in range(1,len(groups)+1):
            if len(groups[i])<totRooms: 
                timeTablesWspace[count] = list(groups.keys())[i-1]
                count+=1
        timeTablesWspace = removeDuplicates(timeTablesWspace)
        #there are no timetables with space, thus we create a new one
        if len(timeTablesWspace) == 0:
            bestOption = len(groups)+1
            if bestOption in group_restrictions[letter]:
                while(bestOption in group_restrictions[letter]):
                    groups[bestOption] = []
                    bestOption += 1 
        #we have timetables with space
        else:
            freeRestrictionTt = {} #getting the free restrictions timetables
            countFree = 0
            for i in range(0, len(timeTablesWspace)):
                if(timeTablesWspace[i] not in group_restrictions[letter]):
                    freeRestrictionTt[countFree] = timeTablesWspace[i]
                    countFree+=1
            #ALL timetables are restricted to this letter
            if len(freeRestrictionTt) == 0 :
                bestOption = len(groups)+1
                if bestOption in group_restrictions[letter]:
                    while(bestOption in group_restrictions[letter]):
                        groups[bestOption] = []
                        bestOption += 1 
            #we have timetables with no restrictions to this letter
            else: 
                lessFull = freeRestrictionTt[0] #choose the one with less elements
                for i in range(1, len(freeRestrictionTt)):
                    if(len(groups[freeRestrictionTt[i]])):
                        if(len(groups[freeRestrictionTt[i]]) < len(groups[bestOption])):
                            if(freeRestrictionTt[i-1] > freeRestrictionTt[i]):
                                lessFull = freeRestrictionTt[i] #stick with first best option
                bestOption = lessFull
    return bestOption
#end nextGroupToFill

def assignGroups(actualRow):
    while not allAssigned(actualRow):# and actualRow < 11:
        zeroIdx = zeroIndex(actualRow) 
        if zeroIdx != -1:
            group = nextGroupToFill(zeroIdx)
            addToGroup(group, chr(97+zeroIdx))
            addRestrictions(group, var[chr(97+zeroIdx)])
            decreaseRelatedColumns(actualRow, zeroIdx)
        else:
            maxIndexValue = cost[actualRow][:].index(max(cost[actualRow][:]))
            group = nextGroupToFill(maxIndexValue)
            addToGroup(group, chr(97+maxIndexValue))
            addRestrictions(group, var[chr(97+maxIndexValue)])
            decreaseRelatedColumns(actualRow, maxIndexValue)
        
        actualRow+=1
        #end if-else conditions
    #end while        
#end assignGroups

def runMaster():
    relations()
    fillCosts()
    addInitialRestrictions(sC)
    assignGroups(0)
    print("Results are stored in 'groups' and in 'cost'")
#end runMaster

runMaster()

        
