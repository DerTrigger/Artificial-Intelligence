# -*- coding: utf-8 -*-
"""
Created on Tue May  1 08:14:53 2018

@author: Guille
"""

''' Examples for implicit Enumeration '''

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
