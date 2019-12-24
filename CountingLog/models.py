##Update to add ResourceLog
##Updated 10/15/18 @ 10:21 @ STEFFLC
##Update Indicator to correctly check missed clocked out. Change from actclockout[n] to Actclockout[n][0] as Actclock out is a dictionary inside a list.
##Actclockout[n] only returns the first dictionary in the list, not the first entry of the dictionary in the list


##Updated 10/16/18 @ 2:13 @ STEFFLC
##Update indicator to even more correctly check missed clock out
## If most recent is missed clock out, skip one op sequence
## If 2nd most recent(but NOT most recent) or later is missed clock out go to next op sequence as usualBack


##Updated 10/17/18 @ STEFFLC
##Update HOLD AREA rules per Luc Villemin

##Update 10/19/18 @ STEFFLC
##Fix hold area rules - fix global rank, add return to resource, assign resource to return object


##Update 10/25/18 @ STEFFLC
##Add bypass in ResourceLog convert function for HOLD AREA as it now has many to one mappings
##I.E. multiple locations now associated with U-HOLD-AREA resource instead of 1:1 mapping

##Update 11/05/18 @ STEFFLC
## Update Global RANK to pull from WO_SCH_PRIORITY which is linked to GLOBAL SCHEDULER
## WORK_ORDER table has correct rank, but it is not what center office uses

##Update 11/05
##add (if actclockout length > 1) check
##Very first op has no prior labor tickets and will error out  as [0][0] index does not exist yet, because no labor tickets exist

##Update 02-14-19
##Add NOTES field so users can write notes in reportview

##Update 02/25/19
##Add OverrideQtys for OPERATION.OVERRIDE_QTYS which details whether user has overriden qty of an op
##Add OpSeqNum which lists the Operation Sequence Number. Chose charField for flexibility rather than integer field.

##Update 02/27/19
##If notes = OVERRIDE you can save anything you want

##Update 04/11/19
##If global rank is >= (instead of >) 30 - U-HOLD-AREA
##Per Beatriz and Jonathan Londono

##UPdate 04/22/19
##If global rank is > 30 - U-HOLD-AREA
##Per Alex and Jonathan London

##Update 05/15/19 
##Add rules for Hold Area Check - if a CNC LATHE or HEAD-FORM is followed by Hot Heading it should never go to Hold Area
##per Luc and Beatriz Jimenez


##Update 7/23/19
##Update rules for Hold Area - Rough Grind can no longer go to Hold Area 2 - only department or VLM
##Head Form(and related) can only go to Hold Area 1 for 1 month period, after that go to VLM
##Add logic for U-HOLD-VLM for resource ID for VLM Machine. Resource ID added by JPN 7/22/19

##Updated 08/15/19 - Remove code which assigns hold shelf location (like 174) to global rank
##for jobs with ranks 8-19
##These are the most urgent jobs and need to remain as normal rank per Alejandro Mendez


##09/23/19 - Update per Jonathan to allow K-RADIAC to go to hold area, VLM

from django.db import models

import pyodbc
from datetime import date
from calendar import monthrange
from django.db.models import Max
import datetime
from django.utils import timezone

# Create your models here.

class CountLog(models.Model):

    EmployeName = models.CharField("Employee Name", max_length=50)
    DateCount = models.DateField("Date of Count", null = True, blank = True )
    LotNo = models.CharField("Lot Number", max_length=20)
    ##Quantity = models.IntegerField(null = True, blank = True)   
    Quantity = models.IntegerField()  #Defaulted previous null to 0
    SupposedQuantity = models.FloatField(null = True, blank = True)   
    ScrapAllowance = models.FloatField(null = True, blank = True)  
    PreviousCount = models.FloatField(null = True, blank = True)  
    GlobalRank = models.IntegerField("Global Rank", null = True, blank = True)   
    MoveTo = models.CharField("Move To Location", max_length=50, null = True, blank = True )
    ArrivedTo = models.BooleanField(default = False)
    MissedClockOut = models.BooleanField("Missed Clock Out (Yes if Missed)", default = False)
    QLabOpen = models.BooleanField("Q-Lab operation is probably open", default = False)
    Notes = models.CharField("Notes", max_length=1000, null = True, blank = True)
    OverrideQtys = models.BooleanField("Is Override_QTY from Operation table selected?", blank = True, default = False)
    OpSeqNum = models.CharField("Operation Sequence Number", max_length=50, null = True, blank = True)
    BelowTargetQty = models.BooleanField("Is the counted QTY < order target qty?", blank=True, default = False)
    DesiredQty = models.IntegerField("WORK_ORDER.DESIRED_QTY:", blank = True, null = True)
    

    
    
    
    def save(self,*args, **kwargs):
        try:
            john = False
            bill = self.Notes[:8]
            if(bill == "OVERRIDE"):
                john = True
        except:
            a = 1 # do nothing
        if (john):
            super(CountLog, self).save(*args, **kwargs)
       
    
    
        elif self.LotNo :
            
            server = 'MSAVMFG1'
            database = 'VMLIVE'
#            database = 'MSA712'

            username = 'tastetf'
            password = 'Vi1234' 
            cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            cursor = cnxn.cursor()
            self.LotNo = self.LotNo.upper() #Capitalize to remove errors. s1 vs S1 in split for example causes problems.
            LotNo = self.LotNo
            
            base,lotsplit = LotNo.split("/")
            try :
                lot,split = lotsplit.split(".")
            except :  
                lot = lotsplit
                split = '0'
                
#inner join min op seq            #cursor.execute("SELECT LABOR_TICKET.ACT_CLOCK_OUT FROM MIN_OP_SEQ INNER JOIN LABOR_TICKET ON MIN_OP_SEQ.WORKORDER_BASE_ID = LABOR_TICKET.WORKORDER_BASE_ID AND MIN_OP_SEQ.WORKORDER_LOT_ID = LABOR_TICKET.WORKORDER_LOT_ID AND MIN_OP_SEQ.WORKORDER_SPLIT_ID = LABOR_TICKET.WORKORDER_SPLIT_ID AND MIN_OP_SEQ.MinRelSeq = LABOR_TICKET.OPERATION_SEQ_NO WHERE LABOR_TICKET.WORKORDER_TYPE = ? AND LABOR_TICKET.WORKORDER_BASE_ID = ? AND LABOR_TICKET.WORKORDER_LOT_ID = ? AND LABOR_TICKET.WORKORDER_SPLIT_ID = ? ORDER BY LABOR_TICKET.OPERATION_SEQ_NO DESC",("W",base,lot,split,))
            #Actclockout = cursor.fetchone()
            
            cursor.execute("SELECT DESIRED_QTY FROM WORK_ORDER WHERE BASE_ID = ? AND LOT_ID = ? AND SPLIT_ID = ? ", (base, lot, split) )
            DESIREDQTY = cursor.fetchall()
            self.DesiredQty = DESIREDQTY[0][0]
            print("desired qty: ", self.DesiredQty)
            
            ##Check to see if entire order is in shortage (not just operatio to operation)
            if (self.Quantity < self.DesiredQty):
                self.BelowTargetQty = True
                

            try:
                CountLog.checkClockOut(base, lot, split, self, cursor)
            except Exception as ex:
                print("ex1: ", ex)
        


            try : 
                cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM EMPLOYEE WHERE ID = ? ",(self.EmployeName,))
                EmpName = cursor.fetchone()
                
                name = str(str(EmpName[0])+"-"+str(EmpName[1]))
                
                self.EmployeName = name
                
            except : 
                self.EmployeName = self.EmployeName
                
            cnxn.close()
            dateadd = date.today() 
            print("dateadd: ", dateadd)
            self.DateCount = dateadd
            super(CountLog, self).save(*args, **kwargs)
            
        
    def __str__(self):
        return "CountLog: {}".format(self.LotNo)
    

    ## self = CountLog object
    ## clockStatus = boolean to be set for MissedClockOut 
    def setClockOut(self, clockStatus):
        """Given object and clocked out status, set that clocked out status to object"""
        self.MissedClockOut = clockStatus
        #print("status inside model: ", self.MissedClockOut)
        
        return
    
    def getClockOut(self):
        """Determine if object is clocked out correctly or not"""
        return self.MissedClockOut
        
    def checkClockOut(base, lot, split, self, cursor):
        """Given a cursor connection to database and a base, lot, split check if the given work order was clocked out
            This will check the most recent operation step, and all previous operation steps for missed clock outs"""
#        print("I'm in check clock out")
        cursor.execute("SELECT ACT_CLOCK_OUT FROM LABOR_TICKET WHERE WORKORDER_TYPE = ? AND WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ? ORDER BY ACT_CLOCK_IN DESC",("W",base,lot,split,))

        Actclockout = cursor.fetchall()
            
        ##Check for Missed Clock Out
        #n=0
        FIRST_ROW = 0
        indicateur = 0
        
        ##Check only the most recent (Actclockout in ASC)
        ##If most recent is clocked out SELECT need to skip the most recent OP as it is not clocked out
        
        if (len(Actclockout) > 1):
            if Actclockout[FIRST_ROW][0] == "" or Actclockout[FIRST_ROW][0] == None :
                    indicateur = 1
#                    print("Checking most recent - ", indicateur)
        
            
        
        ##If there is more than 1 op sequence, and most recent op sequence is clocked in
        ##check remaining op sequences for Miss clock out
        if ( len(Actclockout) >1 and indicateur != 1):
#            print("Checking 2nd and on Op")
#            print("length Actclockout", len(Actclockout))
#            print("Check indicator", indicateur)
 
            rowNum = 1
            while rowNum <= len(Actclockout)-1:
            #For each dictionary pair in the list, get first entry of dictionary which is Actual Clock In time
                #start at Actclockout[1][0] which is 2nd most recent. If this is not clocked out
                if Actclockout[rowNum][0] == "" or Actclockout[rowNum][0] == None :
                    indicateur = 2
                rowNum = rowNum + 1    
#                print("ongoing indicator check: ", indicateur)
                 

################Q-LAB OPEN ########################
        ### Find all with open Q-LAB, including ones where most recent is open Q-LAB(correctly still open)
#        SQLCommand = """ SELECT MIN_OP_SEQ.MinRelSeq, BASE_ID+'/'+LOT_ID+'.'+SPLIT_ID AS 'WORK ORDER', WORK_ORDER.PART_ID AS 'PART ID', PART.MFG_PART_ID AS 'MFG PART ID', PART.DESCRIPTION, WORK_ORDER.GLOBAL_RANK AS 'RANK', WORK_ORDER.DESIRED_WANT_DATE AS 'DUE DATE', WORK_ORDER.DESIRED_QTY AS 'QTY', OPERATION.RESOURCE_ID AS 'LOCATION', WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID, WORK_ORDER.SPLIT_ID
#FROM vmLIVE.dbo.MIN_OP_SEQ MIN_OP_SEQ, vmLIVE.dbo.OPERATION OPERATION, vmLIVE.dbo.PART PART, vmLIVE.dbo.WORK_ORDER WORK_ORDER
#WHERE WORK_ORDER.PART_ID = PART.ID AND WORK_ORDER.BASE_ID = OPERATION.WORKORDER_BASE_ID AND WORK_ORDER.LOT_ID = OPERATION.WORKORDER_LOT_ID AND WORK_ORDER.SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND WORK_ORDER.SUB_ID = OPERATION.WORKORDER_SUB_ID AND WORK_ORDER.TYPE = OPERATION.WORKORDER_TYPE AND MIN_OP_SEQ.WORKORDER_BASE_ID = OPERATION.WORKORDER_BASE_ID AND MIN_OP_SEQ.WORKORDER_LOT_ID = OPERATION.WORKORDER_LOT_ID AND MIN_OP_SEQ.WORKORDER_SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND MIN_OP_SEQ.WORKORDER_SUB_ID = OPERATION.WORKORDER_SUB_ID AND MIN_OP_SEQ.WORKORDER_TYPE = OPERATION.WORKORDER_TYPE AND MIN_OP_SEQ.MinRelSeq = OPERATION.SEQUENCE_NO AND ((WORK_ORDER.TYPE='W') AND (WORK_ORDER.STATUS='R') AND (OPERATION.STATUS='R')) AND OPERATION.RESOURCE_ID = 'Q-LAB' AND WORK_ORDER.BASE_ID = '15-1361' 
#ORDER BY BASE_ID+'/'+LOT_ID+'.'+SPLIT_ID"""                
                
        cursor.execute("SELECT MIN_OP_SEQ.MinRelSeq, BASE_ID+'/'+LOT_ID+'.'+SPLIT_ID AS 'WORK ORDER', WORK_ORDER.PART_ID AS 'PART ID', PART.MFG_PART_ID AS 'MFG PART ID', PART.DESCRIPTION, WORK_ORDER.GLOBAL_RANK AS 'RANK', WORK_ORDER.DESIRED_WANT_DATE AS 'DUE DATE', WORK_ORDER.DESIRED_QTY AS 'QTY', OPERATION.RESOURCE_ID AS 'LOCATION', WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID, WORK_ORDER.SPLIT_ID FROM vmLIVE.dbo.MIN_OP_SEQ MIN_OP_SEQ, vmLIVE.dbo.OPERATION OPERATION, vmLIVE.dbo.PART PART, vmLIVE.dbo.WORK_ORDER WORK_ORDER WHERE WORK_ORDER.PART_ID = PART.ID AND WORK_ORDER.BASE_ID = OPERATION.WORKORDER_BASE_ID AND WORK_ORDER.LOT_ID = OPERATION.WORKORDER_LOT_ID AND WORK_ORDER.SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND WORK_ORDER.SUB_ID = OPERATION.WORKORDER_SUB_ID AND WORK_ORDER.TYPE = OPERATION.WORKORDER_TYPE AND MIN_OP_SEQ.WORKORDER_BASE_ID = OPERATION.WORKORDER_BASE_ID AND MIN_OP_SEQ.WORKORDER_LOT_ID = OPERATION.WORKORDER_LOT_ID AND MIN_OP_SEQ.WORKORDER_SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND MIN_OP_SEQ.WORKORDER_SUB_ID = OPERATION.WORKORDER_SUB_ID AND MIN_OP_SEQ.WORKORDER_TYPE = OPERATION.WORKORDER_TYPE AND MIN_OP_SEQ.MinRelSeq = OPERATION.SEQUENCE_NO AND ((WORK_ORDER.TYPE='W') AND (WORK_ORDER.STATUS='R') AND (OPERATION.STATUS='R')) AND OPERATION.RESOURCE_ID = 'Q-LAB' AND WORK_ORDER.BASE_ID = ? AND WORK_ORDER.LOT_ID = ? AND WORK_ORDER.SPLIT_ID = ? ORDER BY BASE_ID+'/'+LOT_ID+'.'+SPLIT_ID", (base, lot, split,)) 
        astro = cursor.fetchall()
#        print(astro)

        

        cursor.execute("SELECT WORKORDER_BASE_ID+'/'+WORKORDER_LOT_ID+'.'+WORKORDER_SPLIT_ID AS 'WORK ORDER', LAST_CLOSED_OPERATION.LAST_SEQ_NO_CLOSED, WORKORDER_BASE_ID, WORKORDER_LOT_ID, WORKORDER_SPLIT_ID FROM VMLIVE.dbo.LAST_CLOSED_OPERATION LAST_CLOSED_OPERATION, VMLIVE.dbo.WORK_ORDER WORK_ORDER WHERE LAST_CLOSED_OPERATION.WORKORDER_BASE_ID = WORK_ORDER.BASE_ID AND LAST_CLOSED_OPERATION.WORKORDER_LOT_ID = WORK_ORDER.LOT_ID AND LAST_CLOSED_OPERATION.WORKORDER_SPLIT_ID = WORK_ORDER.SPLIT_ID AND LAST_CLOSED_OPERATION.WORKORDER_SUB_ID = WORK_ORDER.SUB_ID AND LAST_CLOSED_OPERATION.WORKORDER_TYPE = WORK_ORDER.TYPE AND ((WORK_ORDER.STATUS='R')) AND WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ?", (base, lot, split,) )
        roger = cursor.fetchall()
        
        
#        print(roger)
        
        ##If MIN_OP_SEQ (open, Q-LAB) is less than most recent closed we know that Q-LAB, open preceeds a closed operation which is bad
        try:
            if (astro[0][0] < roger[0][1]):
#                print("astro from MINRelSeq: ", astro[0][0])
#                print("roger from last closed op: ", roger[0][1])
#                print("match")
                self.QLabOpen = True
        except IndexError:
            self.QLabOpen = False
        except:
            self.QLabOpen = False
################################################################

        #MOST RECENT OPERATION STILL OPEN
        if indicateur == 1 :
#            print("indicateur = 1", indicateur)
            self.MissedClockOut = True
            
            ######!!!! if and else execute SQL statements are NOT identical!!!####################
            cursor.execute("SELECT OPERATION.RESOURCE_ID, OPERATION.CALC_END_QTY, OPERATION.CALC_START_QTY, OPERATION.SEQUENCE_NO, OPERATION.OVERRIDE_QTYS FROM MIN_OP_SEQ INNER JOIN OPERATION ON MIN_OP_SEQ.WORKORDER_BASE_ID = OPERATION.WORKORDER_BASE_ID AND MIN_OP_SEQ.WORKORDER_LOT_ID = OPERATION.WORKORDER_LOT_ID AND MIN_OP_SEQ.WORKORDER_SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND MIN_OP_SEQ.MinRelSeq < OPERATION.SEQUENCE_NO WHERE OPERATION.WORKORDER_TYPE = ? AND OPERATION.WORKORDER_BASE_ID = ? AND OPERATION.WORKORDER_LOT_ID = ? AND OPERATION.WORKORDER_SPLIT_ID = ? ORDER BY OPERATION.SEQUENCE_NO ASC",("W",base,lot,split,))
#            cursor.execute("SELECT OPERATION.RESOURCE_ID, OPERATION.CALC_END_QTY, OPERATION.CALC_START_QTY  FROM MIN_OP_SEQ INNER JOIN OPERATION ON MIN_OP_SEQ.WORKORDER_BASE_ID = OPERATION.WORKORDER_BASE_ID AND MIN_OP_SEQ.WORKORDER_LOT_ID = OPERATION.WORKORDER_LOT_ID AND MIN_OP_SEQ.WORKORDER_SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND MIN_OP_SEQ.MinRelSeq = OPERATION.SEQUENCE_NO WHERE OPERATION.WORKORDER_TYPE = ? AND OPERATION.WORKORDER_BASE_ID = ? AND OPERATION.WORKORDER_LOT_ID = ? AND OPERATION.WORKORDER_SPLIT_ID = ? ORDER BY OPERATION.SEQUENCE_NO ASC",("W",base,lot,split,))

            CountLog.doStuff(base, lot, split, self, cursor)
        
        ##2nd most recent (or later) operation still open
        #If indicator = 2 then Missed clock out, but do NOT skip most recent OP
        elif indicateur == 2:
#            print("indicateur = 2", indicateur)
            self.MissedClockOut = True
            cursor.execute("SELECT OPERATION.RESOURCE_ID, OPERATION.CALC_END_QTY, OPERATION.CALC_START_QTY, OPERATION.SEQUENCE_NO, OPERATION.OVERRIDE_QTYS  FROM MIN_OP_SEQ INNER JOIN OPERATION ON MIN_OP_SEQ.WORKORDER_BASE_ID = OPERATION.WORKORDER_BASE_ID AND MIN_OP_SEQ.WORKORDER_LOT_ID = OPERATION.WORKORDER_LOT_ID AND MIN_OP_SEQ.WORKORDER_SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND MIN_OP_SEQ.MinRelSeq = OPERATION.SEQUENCE_NO WHERE OPERATION.WORKORDER_TYPE = ? AND OPERATION.WORKORDER_BASE_ID = ? AND OPERATION.WORKORDER_LOT_ID = ? AND OPERATION.WORKORDER_SPLIT_ID = ? ORDER BY OPERATION.SEQUENCE_NO ASC",("W",base,lot,split,))

            CountLog.doStuff(base, lot, split, self, cursor)
            
        ##Everything clocked out correctly
        else : 
#            print("indicateur: ", indicateur)
            cursor.execute("SELECT OPERATION.RESOURCE_ID, OPERATION.CALC_END_QTY, OPERATION.CALC_START_QTY, OPERATION.SEQUENCE_NO, OPERATION.OVERRIDE_QTYS  FROM MIN_OP_SEQ INNER JOIN OPERATION ON MIN_OP_SEQ.WORKORDER_BASE_ID = OPERATION.WORKORDER_BASE_ID AND MIN_OP_SEQ.WORKORDER_LOT_ID = OPERATION.WORKORDER_LOT_ID AND MIN_OP_SEQ.WORKORDER_SPLIT_ID = OPERATION.WORKORDER_SPLIT_ID AND MIN_OP_SEQ.MinRelSeq = OPERATION.SEQUENCE_NO WHERE OPERATION.WORKORDER_TYPE = ? AND OPERATION.WORKORDER_BASE_ID = ? AND OPERATION.WORKORDER_LOT_ID = ? AND OPERATION.WORKORDER_SPLIT_ID = ? ORDER BY OPERATION.SEQUENCE_NO ASC",("W",base,lot,split,))

            CountLog.doStuff(base, lot, split, self, cursor)
        return
    
    def doStuff(base, lot, split, self, cursor):
        """Main action function within the save function. Most actions performed here"""
        Resource = cursor.fetchone()
        allResource = cursor.fetchall()
        print("allResource: ", allResource)
#        print("allResource1: ", allResource[0])
        print("Resource: ", Resource)
#        print("Resource: ", Resource)
        resource = str(Resource[0]) ##Operation.Resource_ID
        opseqno = str(Resource[3]) ##Operation.Sequence_NO of resource
        print("resource: ", resource, "for opseq# ", opseqno)
#        print("resource: ", resource)
        supquantity = int(Resource[1]) ##Calc End Qty
        self.SupposedQuantity = supquantity
        #print("supquant----------", supquantity)
        startqty = int(Resource[2]) ##Calc Start Qty
        if(Resource[4] =='Y'):
            self.OverrideQtys = True
        elif(Resource[4]=='N'):
            self.OverrideQtys = False
            
#        print("overrideqtys: ", self.OverrideQtys)
        self.OpSeqNum = str(Resource[3])
#        print("Op Seq Num: ", self.OpSeqNum)
        
        
        scrapallowance = startqty-supquantity ##This takes into account FIXED_SCRAP_UNITS and SCRAP_YIELD_PCT (I.E. flat + % scrap)
        
        CountLog.acquireRank(base, lot, split, self, cursor)
#        resource = CountLog.checkHoldAreaOverride(resource, base, lot, split, self, cursor)
        resource = CountLog.checkHoldAreaOverride(resource, base, lot, split, self, cursor, opseqno)
        


        beginMaxID = CountLog.objects.filter(LotNo=self.LotNo)             
        InterMaxID = beginMaxID.aggregate(Max('id'))
        Maxid = InterMaxID.get('id__max', 0)
        Maxid = CountLog.objects.filter(LotNo=self.LotNo).aggregate(Max('id')).get('id__max', 0)
        
        try:
            Countprevious = CountLog.objects.get(id = Maxid)
            prevcount = Countprevious.Quantity
            
            if prevcount == "" or prevcount == None : 
                prevcount = 0
            
            
            #print("previous count-------", prevcount)
        except:
            #print("except loop----------")
            prevcount = 0
        

        self.PreviousCount = prevcount
        scrapallowance = prevcount - scrapallowance
        self.MoveTo = str(ResourceLog.convert(resource))
#        print("CONVERT LOG Converted MoveTo ============", self.MoveTo)
        self.ScrapAllowance = scrapallowance
        
        return
        
    
        ## http://codegist.net/snippet/python/eomonthpy_indepndnt_python
        ## Replicates Excel EOMONTH function
        ## EOMONTH function will return a DATE object representing the last day
    def eomonth(start_date, months):
        """Return the date of the last day of the month before or after a specified number of months."""
        assert isinstance(start_date, date)
        years = int(months / 12)
        months -= years * 12
        m = start_date.month + months
        y = start_date.year + years
        if m < 1:
            m, y = m + 12, y - 1
        elif m > 12:
            m, y = m - 12, y + 1
        d = monthrange(y, m)[1]
        return date(y, m, d)
    
    def acquireRank(base, lot, split, self, cursor):
        """given work order(base, lot, split) and database cursor, acquire global rank of given work order """
        
        ##WO_SCH_PRIORITY is linked to GLOBAL SCHEDULER
        cursor.execute("SELECT GLOBAL_RANK FROM WO_SCH_PRIORITY WHERE SCHEDULE_ID = ? and WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ? ", ("STANDARD", base, lot, split,) )


            #WORK_ORDER table is not linked to GLOBAL SCHEDULER
#        cursor.execute("SELECT GLOBAL_RANK FROM WORK_ORDER WHERE BASE_ID = ? AND LOT_ID = ? AND SPLIT_ID = ? ",(base,lot,split,))
        
        Globalrank = cursor.fetchone()
        rank = int(Globalrank[0])
#        print("rank: ", rank)
        self.GlobalRank = rank
        return
    
    '''
    check if the next resource in line should be overridden.
    Sometimes operations like HEAD-FORM need to go to HOLD AREA instead if
    global rank is high enoug hand customer want date is far enoug hout
    
    resource = the next open resource from Operation Table
    base = base ID (18-1234)
    lot = Lot ID (/1)
    split = Split ID(.0)
    self = self reference
    cursor = cursor connection to Visual
    opseqno = Operation Sequence Number of the next resource ID from Operation Table
    '''
    
    
    
    def checkHoldAreaOverride(resource, base, lot, split, self, cursor, opseqno):
        cursor.execute("SELECT DESIRED_WANT_DATE FROM WORK_ORDER WHERE BASE_ID = ? AND LOT_ID = ? AND SPLIT_ID = ? ",(base,lot,split,)) 
        wantDateObject = cursor.fetchone()
        wantDate = wantDateObject[0].date() #This is a date object which is comparable 
        
        ##7/22/19 - VLM Machine added Need logic on when to send items there
        ##Examples from Jonathan M via Igor Given 7/22 or 7/23 date
        ##Rough Grind up <= 12/31 goes to department 1/1/2020 and after goes to VLM
        
        ##Head Form 8/1 to 8/31 goes to HOLD AREA 1
        ##Head Form 9/1 and after goes to VLM
        
        
        
#        grindDate = CountLog.eomonth(date.today(), 2) ##Cannot go to Hold Area 2
        CNCDate = CountLog.eomonth(date.today(), 0)
        ###VLM Grind Date is currently same as grind date
        VLMGrindDate = CountLog.eomonth(date.today(), 5)
        VLMCNCDate = CountLog.eomonth(date.today(), 1)

        #Example today 09/23/19
        #radiacVLMDate = 1/31/20
        #radiacHoldDate = 12/31/19
        radiacHoldDate = CountLog.eomonth(date.today(), 3)
        radiacVLMDate = CountLog.eomonth(date.today(), 4)


        resourceOriginal = resource ##Store the original resource value
        print("resourceOriginal: ", resourceOriginal)
#        print("grind days", grindDays)
        print("want date", wantDate)
        #print("DeltaDays: ", deltaDays)
        
        
#        print("grind Date = ", grindDate)
        print("CNC Date = ", CNCDate)
        print("VLMGrindDate: ", VLMGrindDate)
        print("VLMCNCDate: ", VLMCNCDate)


#        If ({OPERATION.RESOURCE_ID} = “G-CENTRLS-ROUGH”) and ({WORK_ORDER.DESIRED_WANT_DATE} >= EOMONTH(TODAY(),2)) and ({WORK_ORDER.GLOBAL_RANK} > 22)
#        then “MOVE TO HOLD AREA”
#        if self.GlobalRank > 30 and resource == "G-CENTRLS-ROUGH" and (wantDate >= grindDate ):
#            resource = "U-HOLD-AREA2"
        
        if self.GlobalRank > 30 and resource == "G-CENTRLS-ROUGH" and (wantDate >= VLMGrindDate ):
            resource = "U-HOLD-VLM"

        # if self.GlobalRank > 30 and resource == "K-RADIAC" and (wantDate >= radiacVLMDate):
        #     resource = "U-HOLD-VLM"
        #Make sure you put VLM first OR put bounds on Hold Area (>X, < Y)
        if self.GlobalRank > 30 and resource == "K-RADIAC":
            if(wantDate > radiacVLMDate):
                resource = "U-HOLD-VLM"
            elif(wantDate > radiacHoldDate):
                resource = "U-HOLD-AREA"

        #If Point, head form, or lathe
#        If ({OPERATION.RESOURCE_ID} = “S-CNC-LATHE”) or ({OPERATION.RESOURCE_ID} = “POINT”) or ({OPERATION.RESOURCE_ID} = “HEAD-FORM”) and ({WORK_ORDER.DESIRED_WANT_DATE} >= EOMONTH(TODAY(),0)) and ({WORK_ORDER.GLOBAL_RANK} > 22)
#        then “MOVE TO HOLD AREA”
#        Else MOVE TO NEXT OPERATION.
        if self.GlobalRank > 30 and resource == "POINT" :
            if(wantDate > VLMCNCDate ):
                resource = "U-HOLD-VLM"
            elif(wantDate > CNCDate) :
                resource = "U-HOLD-AREA"
            
        ##IDentical to Point logic, except these operations need to SKIP HOLD AREA if succeeded by any HOT HEADING operation (H-PRESS235, H-PRESS60,H-PRESS95, H-IMPACT)
        
            
        
        
        if self.GlobalRank > 30 and resource == "S-CNC-LATHE"  \
        or self.GlobalRank > 30 and resource == "HEAD-FORM" \
        or self.GlobalRank > 30 and resource == "S-DRILL" :
            if(wantDate > VLMCNCDate):
                resource = "U-HOLD-VLM"
            elif(wantDate > CNCDate):
                resource = "U-HOLD-AREA" 
            
            cursor.execute("SELECT RESOURCE_ID, SEQUENCE_NO FROM OPERATION WHERE WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ?", (base, lot, split))
            allResource = cursor.fetchall()
            opseqno = int(opseqno)
            for rsrc in allResource:
                if rsrc[0] == "H-PRESS235":
                    hPress235Sequence = rsrc[1]
                    if(hPress235Sequence > opseqno):
                        print("This will eventually go to H-PRESS 235, do not override HOLD AREA")
                        resource = resourceOriginal 
                if rsrc[0] == "H-PRESS60":
                    hPress60Sequence = rsrc[1]
                    if(hPress60Sequence > opseqno):
                        print("This will eventually go to H-PRESS 60, do not override HOLD AREA")
                        resource = resourceOriginal 
                if rsrc[0] == "H-PRESS95":
                   hPress95Sequence = rsrc[1]
                   if(hPress95Sequence > opseqno):
                       print("This will eventually go to H-PRESS 95, do not override HOLD AREA")
                       resource = resourceOriginal                    
                   
                if rsrc[0] == "H-IMPACT":
                   hImpactSequence = rsrc[1]
                   if(hImpactSequence > opseqno):
                       print("This will eventually go to H-Impact, do not override HOLD AREA")
                       resource = resourceOriginal   
                                       
        return resource
    

## Resource ID and Port of Entry pairs manually entered into Admin interface
## This class / table serves to hold and convert pairs of resource ID to port of entry
class ResourceLog(models.Model):
    PortEntry = models.CharField(max_length = 50)    
    ResourceID = models.CharField(max_length = 30)  
    
    ## Given a resourceID, i.e. G-CENTRLS-ROUGH
    ## convert to Port of Entry, i.E. Rough Grind
    def convert(resource):
        if resource != "U-HOLD-AREA":
            port = ResourceLog.objects.get(ResourceID = resource)
            return port.PortEntry.upper() #send always uppercase
        
        
        #HOLD AREA PROGRAM USES MANY TO 1 relationship
        #Cannot use "GET" as it only allows for one result
        if resource == "U-HOLD-AREA":
            port = ResourceLog.objects.filter(ResourceID = resource)
            port = port[0] # THIS will return a RESOURCE log object

            port = str(port)
            return port
            
        

    
    def __str__(self):
        return self.PortEntry
    

    
    
class Pipeline(models.Model):
    ##Idea - each Pipeline model has several PipelineCounts
    ##When done - take workOrder, finishPipelineBadge, totalCount -> input into Count
    workOrder = models.CharField(max_length = 20)
    originalWorkOrder = models.CharField(max_length = 20, null = True, blank = True) #Keep a copy of the original WO in case someone changes it by accident (or not accident)
    opSequenceFrom = models.IntegerField() ##Probably max length 3
    opSequenceTo = models.IntegerField() #Probably max length 3
#    WOOPkey = models.CharField(null = True, blank = True)
    dateCreated = models.DateTimeField(auto_now_add = True)
    totalCount = models.IntegerField(blank = True, null = True) ##PRobably max length 5
    
    dateCount1 = models.DateTimeField(blank=True, null=True)
    quantity1 = models.IntegerField(default = 0, blank=True, null=True)
    sampleSize1 = models.IntegerField(default = 0, blank=True, null=True)
    buyOffBadge1 = models.IntegerField(default = 0, blank=True, null=True)
    buyOffPerson1 = models.CharField(max_length = 150, blank=True, null = True)
    
    dateCount2 = models.DateTimeField(blank = True, null = True)
    quantity2 = models.IntegerField(default = 0)
    sampleSize2 = models.IntegerField(default = 0, blank = True)
    buyOffBadge2 = models.IntegerField(default = 0, blank = True)
    buyOffPerson2 = models.CharField( max_length = 150, blank=True, null = True)  

    dateCount3 = models.DateTimeField(blank = True, null = True)
    quantity3 = models.IntegerField(default = 0)
    sampleSize3 = models.IntegerField(default = 0, blank = True)
    buyOffBadge3 = models.IntegerField(default = 0,blank = True)
    buyOffPerson3 = models.CharField( max_length = 150, blank=True, null = True)  
    
    dateCount4 = models.DateTimeField(blank = True, null = True)
    quantity4 = models.IntegerField(default = 0)
    sampleSize4 = models.IntegerField(default = 0, blank = True)
    buyOffBadge4 = models.IntegerField(default = 0, blank = True)
    buyOffPerson4 = models.CharField( max_length = 150, blank=True, null = True) 
    
    pipelineClosed = models.BooleanField(default = False)
    

    
    def save(self,*args, **kwargs):
        
        old = Pipeline.objects.get(id=self.id)
#        if old:
#            print("old qty: ", old.quantity1)
#            print("current: ", self.quantity1)
#            print("old date: ", old.dateCount1)

        
        server = 'MSAVMFG1'
        database = 'VMLIVE'
#            database = 'MSA712'

        username = 'tastetf'
        password = 'Vi1234'
        cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)


          
        if(old.buyOffBadge1 != self.buyOffBadge1):
            self.buyOffPerson1 = Pipeline.lookupName(self.buyOffBadge1, cnxn)
            
        if(old.buyOffBadge2 != self.buyOffBadge2):
            self.buyOffPerson2 = Pipeline.lookupName(self.buyOffBadge2 , cnxn)
            
        if(old.buyOffBadge3 != self.buyOffBadge3):
            self.buyOffPerson3 = Pipeline.lookupName(self.buyOffBadge3, cnxn)
            
        if(old.buyOffBadge4 != self.buyOffBadge4):
            self.buyOffPerson4 = Pipeline.lookupName(self.buyOffBadge4 , cnxn)  
        

        if(not old.workOrder):
            self.originalWorkOrder = self.workOrder  
            
#        print("self.dateCount1, D", self.dateCount1)
#########################
        if(old.quantity1 != self.quantity1):
            self.dateCount1 = datetime.datetime.now(tz=timezone.utc)
            print("doing stuff1")
            ###########################
        else:
            self.dateCount1 = old.dateCount1
        if(old.quantity2 != self.quantity2):
            self.dateCount2 = datetime.datetime.now(tz=timezone.utc)
            print("doing stuff2") 
        else:
            self.dateCount2 = old.dateCount2
#        print("self.dateCount1, F", self.dateCount1)
        if(old.quantity3 != self.quantity3):
            self.dateCount3 = datetime.datetime.now(tz=timezone.utc)
            print("doing stuff3")
        else:
            self.dateCount3  = old.dateCount3
#        print("self.dateCount1, G", self.dateCount1)
        if(old.quantity4 != self.quantity4):
            self.dateCount4 = datetime.datetime.now(tz=timezone.utc)
            print("doing stuff4") 
        else:
            self.dateCount4 = old.dateCount4
        
        
        
        
#        print("self.dateCount1, H", self.dateCount1)
        
        self.totalCount = self.quantity1 + self.quantity2 + self.quantity3 + self.quantity4
        super(Pipeline, self).save(*args, **kwargs)
        new = Pipeline.objects.get(id=self.id)
        if new:
            print("new: ", new.quantity1)
            print("new date: ", new.dateCount1)

        cnxn.close()
        

    def __str__(self):
        return self.workOrder
    
    def lookupName(badge, cnxn):
            cursor = cnxn.cursor()
            try : 
                cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM EMPLOYEE WHERE ID = ? ",(badge,))
                EmpName = cursor.fetchone()
                
                name = str(str(EmpName[0])+"-"+str(EmpName[1]))
                
                person = name
                print("name: ", name)
            except : 
                print("no match")
                person = None        
            return person
    
    
