# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 15:01:21 2022

@author: Harold
"""
import sys
from enum import Enum
from geograpy import get_geoPlace_context

# Takes a string and returns locational information

# the 3countries



class unknownC(Enum):
    # uninitialized
    UNKNOWN = 101
    # known to be private
    PRIV = 102
    # unknown to be not available
    NA = 103
    # invalid value
    NL = 104
    # Joke
    JK = 105
    # maximum number of records in run
    MX = 106
    
# informal GeoNames

class GeoCasual:
    def __init__(self):
        pass
    def isJoke(self,rawLoc):
        if "Nowhere" in rawLoc:
            return True
        if "Everywhere" in rawLoc:
            return True
        if "Politics" in rawLoc:
            return True
        if "Knowledge" in rawLoc:
            return True
        if "Goblinarium" in rawLoc:
            return True
        if "Global" in rawLoc:
            return True
        # may be worthwhile going back to web addresses later
        if "https" in rawLoc:
            return True
        if "Miles away" in rawLoc:
            return True
        if "Sweateronbackwards" in rawLoc:
            return True
        if "plague" in rawLoc:
            return True
        if "Past2Future" in rawLoc:
            return True
        return False
    def isCan(self,rawLoc):
        if "amiskwacîwâskahikan" in rawLoc:
            return True
        if "PERTH, ON" in rawLoc:
            return True
        if "Brossard" in rawLoc:
            return True
    def isUS(self,rawLoc):
        if "NYC" in rawLoc:
            return True
        if "USA" in rawLoc:
            return True
        if "Washington" in rawLoc:
            return True
        if "Maine" in rawLoc:
            return True
        if "seattle" in rawLoc:
            return True
        if "Singleville AR" in rawLoc:
            return True
        if "Santa Barbara, CA" in rawLoc:
            return True
        if "HoCo CA" in rawLoc:
            return True
        if "greensburg, pa" in rawLoc:
            return True
        if "Orange County, CA" in rawLoc:
            return True        
        return False
    def isNonUS_Can(self,rawLoc):
        if self.isAustralia(rawLoc):
            return True
        if self.isUK(rawLoc):
            return True
        if self.isDEU(rawLoc):
            return True
        return False
    def isAustralia(self,rawLoc):
        if "Australia" in rawLoc:
            return True
        if "Wurundjeri" in rawLoc:
            return True
        return False
    def isUK(self,rawLoc):
        if "Gweriniaeth" in rawLoc:
            return True
        if "London England" in rawLoc:
            return True
        if "Worcestershire UK" in rawLoc:
            return True
        return False
    def isDEU(self,rawLoc):
        if " DEU " in rawLoc:
            return True
        if "NRW" in rawLoc:
            return True
        if "Niederrhein" in rawLoc:
            return True
        return False
    def isFJT(self, rawLoc):
        if " FJT " in rawLoc:
            return True
        return False

class C3:
    def __init__(self,useNLTK=False,useGEOGRPY=False,mxREC = 100000000000):
       """ Determine country from text location string.
       
       Creates object given in response to location field is classified as either
       Canadian, American or Other
       
       Parameters
       __________
       useNLTK  : bool
           Make use of the NLTK library
       useGEOGRPY : bool
           Make use of the geograpy
       mxREC : int
           Maximum number of records to process
           
       Examples
       ________
       >>>  MyC3 = C3()
       """ 
       self.retval = unknownC.UNKNOWN
       self.country = unknownC.UNKNOWN
       self.CAN = 11
       self.US = 12
       self.OTHER = 13
       self.useNLTK = useNLTK
       self.useGEOGRPY = useGEOGRPY
       self.MAXREC = mxREC
       # Number of records search for in session
       self.RecNo = 0
       self.CasCoun = GeoCasual()
    def getC3(self,rawLoc):
       
        self.RecNo += 1
        # two stage exit
        # first warn max is hit
        if self.RecNo == self.MAXREC:
            print('RecNo = ',self.RecNo)
            return unknownC.MX
        # second halt operation
        if self.RecNo > self.MAXREC:
            print('RecNo = ',self.RecNo)
            sys.exit('Maximum Record Hit of ')
        # give Canada Priority
        if self.isCan(rawLoc):
            return self.CAN
        # if it is not Canadian and 
        # we are not going to use NLTK then unknown
        if self.CasCoun.isJoke(rawLoc):
            return unknownC.JK
        if self.CasCoun.isNonUS_Can(rawLoc):
            return self.OTHER
        if self.useGEOGRPY is False:
            return self.OTHER
        if self.isUS(rawLoc) is True:
             return self.US
        return self.OTHER
    def isUS(self,rawLoc):
        if self.CasCoun.isUS(rawLoc):
            return True
        try:
            if self.places.countries[0] == 'United States of America':
                return True
            else:
                return False
        except:
            print('error rawLoc invalid',rawLoc)
            return False
    def isCan(self,rawLoc):
        if "Canada" in rawLoc:
            return True
        if ",Can " in rawLoc:
            return True
        if "ALBERTA" in rawLoc:
            return True
        if "canada" in rawLoc:
            return True
        if self.CasCoun.isCan(rawLoc):
            return True
        if self.useGEOGRPY == False: 
          return False
        # from this point on use geograpy
        # unable to install properly
        self.places = get_geoPlace_context(text=rawLoc)
        try:
            if self.places.countries[0] == "Canada":
                return True
        except:
            return False
        self.country = self.places.countries[0]
        
        return False
            


    
         
