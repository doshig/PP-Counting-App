###Updated 10/25/18 @ STEFFLC
##Add new LotCount filter instead of get. Get only allows 1 return object
##Filter is multiple. This allows program to function in event there are multiple WO enteredd all with not arrived status
##I.E. duplicates for testing, or duplicates from user error

##Update to match any department entry 100-155 to HOLD AREA1 (main)
##Update to match any department entry 156-168 to HOLD AREA2 (grind)
##Update Department to 50 characters, Dimensional inspection is >20


##Update 11/05/18
##Overrite global rank on VISUAL live server to the physical inventory location
##in hold area. I.E. shelf 102 will set global rank to 102 for HOLD AREA1
## Can deliver HOLD AREA2 items to HOLD AREA1 now


##Update 11/05/18
##Update GLOBAL RANK To update to WO_SCH_PRIORITY table instead of WORK_ORDER
##CEnter office pulls/writes data into WO_SCH_PRIORITY which is GLOBAL SCHEULDER

##Update 11/6/18
##allow certain things to go to POINT or HEAD FORM 
##single angle, double angle, bolt size means departments could be mixed and matched a bit per Dennis K.


##Update 11/7/18
##Change list to [" dslkdf" ] to fix list implementation

##Also update to allow washing station logic to go to following department

##Update 11/08/18
##Add additional logic to accept short barcodes
##Really long barcodes do not seem to scan well, like DIMENSIONAL INSPECTION
## All D INSPC instead, for example

##Update 12/10/18
##Allow Hold Area 2 nito area 1 for overflow
## Add new Hold Area 1 locations for new rack.
## Convert maps to lists


##Update 03/12/19 - Add upper method to remove case discrepancies

##Update 04/18/19 - Fix MAIN_HOLD_AREA_LIST / GRIND_HOLD_AREA_LISt duplicate - hold 2 was only accepting hold 1 locations


##Update 06/05/19 - Add update to Department log to accept 'COUNTING' as override to any operation
##For example, if it says deliver to OP, but COUNTING is entered it will validate
##This is primarily for LAB who delivers jobs to Counting.


##Update 06/14/2019 - Add update  - fix issue where COUNTING would not be accpeted
## If code already adds a "Alternate Location" such as D INSPC for DIMENSIONAL INSPECTION
##Code now checks for counting before anything else

##Update 06/26/1i - Allow Heat Treat for Q-LAB. In very rare cases HARDNESS TEST shows Q-LAB but must go to HEAT TREAT according to
##Jonathan M


###Update 07/19/19 -             GRIND_HOLD_AREA_LIST = list(map(str, range(155, 169))) change upper bound to 169 so the range is 155-168.
### Add Locations for tall roll-y carts to main hold area per Jonathan M(Londono)
### list(map(str, range(169, 175))) - > list(map(str, range(169, 178))) #add 175, 176, 177 one for end of each main hold area row


##07/22/19 - Add new logic for the VLM - vertical lift near Heat Treat department.

##07/24/19 - Some Hold area racks were re-purposed to center of grind - Rough and Finish Grind. Update Numbers accordingly.
##E.G. 156 rack can now be accepted for Rough Grind
##169 for Finish Grind

##07/26/19 - Do not allow 'HOLD AREA1' OR 'HOLD AREA2'. Only allow barcode on shelf I.E. 159, etc.

##07/29/19 -                                     + list(map(str,range(137, 143))) fixed this previously was not included for rough grind list


##07/29/19 -update 2 - add 6x more locations for ROUGH GRIND per Jonathan Londono

##08/07/19 - Fix error with isinstance. Some instances of department were strings of integers, not integers



##Updated 08/15/19 - Remove code which assigns hold shelf location (like 174) to global rank
##for jobs with ranks 8-19
##These are the most urgent jobs and need to remain as normal rank per Alejandro Mendez


from django.db import models
import pyodbc

from CountingLog.models import CountLog, ResourceLog

# Create your models here.


class DepartmentLog(models.Model):

    Date = models.DateTimeField(auto_now = True)
    EmployeName = models.CharField(max_length=50)
    LotNo = models.CharField(max_length=20)
    Department = models.CharField(max_length=50)
    WrongLocation = models.BooleanField(default = False)
    CorrectDept = models.CharField(max_length=100, blank=True, null = True ) #Added 1/18/19 for better error reporting
    AllowedDepts = models.CharField(max_length=500, blank=True, null = True, default = "None")
    DeptGlobalRank = models.CharField(max_length = 50, blank = True)
    Notes = models.CharField(max_length = 250, blank = True)
    ##CorrectDept is from CountingLog model.
    
    def save(self,*args, **kwargs):
    
        
        if self.LotNo :
            
            lotno = self.LotNo
            server = 'MSAVMFG1'
            database = 'VMLIVE'
#            database = 'MSA712'
            username = 'stefflc'
            password = 'buttpain1'    
            cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            cursor = cnxn.cursor()
            print("selflotno: ", self.LotNo)
            base,lotsplit = self.LotNo.split("/")
            try :
                lot,split = lotsplit.split(".")
            except :  
                lot = lotsplit
                split = '0'
            
            
            
            MAIN_HOLD_AREA_LIST = list(map(str, range(100, 155))) #+ list(map(str, range(169, 178)))
#            GRIND_HOLD_AREA_LIST = list(map(str, range(155, 169)))
            
            
            '''
            Recall that range is NOT inclusive of the final number Y (X, Y)
            Ranges are:
            #156- 161 
            #143 - 148
            #137 - 142
            #175-180 (6 spots)
            '''
            ROUGH_GRIND_AREA_LIST = list(map(str,range(156, 162))) \
            + list(map(str,range(143, 149))) \
                                    + list(map(str,range(137, 143))) \
                                    + list(map(str, range(175, 184)))
            '''#169 - 174
            #162 - 167'''
            FINISH_GRIND_AREA_LIST = list(map(str,range(169, 175))) \
                                    + list(map(str,range(162, 168))) 
            
            
            VLM_HOLD_AREA_LIST = ["VLM"]

            
            POINT_LIST = ["POINTING TRAUB"]
            HEAD_FORM_LIST = ["HAND TRAUB", "AUTO TRAUB", "ROBOTS", "CNC LATHE"]
            WASHING_LIST = ["FILLET ROLL", "HEAT TREAT", "PASSIVATION", "THREAD ROLL"]
            DIMENSIONAL_LIST = ["D INSPC"]
            VISUAL_LIST = ["V INSPC"]
            CROSSDRILL_LIST = ["XDRILLD"]
            QUALITY_ENG_LIST = ["Q ENG"]
            SLUG_GRIND_LIST = ["SLUG GRIND", "SLUG GR"]
            LUBE_LIST = ["SAND BLASTING"] ## ADded 01_24_19
            RADIAC_LIST = ["RADIAC"] ##Added 04_03_19
            THREAD_ROLL_LIST = ["TROLL"] ##Added 04_03_19
            FILLET_ROLL_LIST = ["FROLL"] ##Added 04_03_19
            COUNTING_LIST = ["COUNTING"] ##Added 06/05/19 for LAB to deliver to counting
            LAB_LIST = ["HEAT TREAT"]
            
            
            MAIN_HOLD_AREA = "HOLD AREA1"
#            GRIND_HOLD_AREA = "HOLD AREA2"
            VLM_HOLD_AREA = "VLM"
            ROUGH_GRIND_AREA = "ROUGH GRIND"
            FINISH_GRIND_AREA = "FINISH GRIND"
            ralphio = ResourceLog.objects.all()
            ALL_PORTS = list()
            for port in ralphio:
#                print("port: ", port.PortEntry)
                ALL_PORTS.append(port.PortEntry)
#            print("ALL_PORTS: ", ALL_PORTS)
                
            
            
       
            self.LotNo = self.LotNo.upper() ###Capitalize to remove errors. s1 vs S1 in split for example causes problems.
            lotno = self.LotNo
            
#            try:
#            LotCount = CountLog.objects.get(LotNo = lotno, ArrivedTo = False) #PRODUCTION CODE , ONLY GETS 1
            LotCount = CountLog.objects.filter(LotNo = lotno, ArrivedTo = False)
            print("1 LotCount: ", LotCount)
            LotCount = LotCount.latest('id') #GETS MOST RECENT LOG IF MULTIPLE ARE OPEN
            print("2 LotCount: ", LotCount)
            correctdept = LotCount.MoveTo
            
            
            
            ##I'm deliberately getting rank from counting log
            ##Assumption is that department log object is created very shortly after counting log
            ##It is very unlikely that global rank will change between count and dept log
            ##It is not worth doing an additional database query to get rank again at dept log step
            self.DeptGlobalRank = LotCount.GlobalRank
            print("self.DeptGlobalRank", self.DeptGlobalRank)
            self.CorrectDept = correctdept
            
            print("correctdept: ", correctdept)
            print("self.Department: ", self.Department)


                
                
#            print("correct dept ---------------------", correctdept)  #For testing only
#            print("1",correctdept)
#            print("type1: ", type(correctdept))
#            print("test equality", (self.Department == "HOLD AREA1"))
            
            
#            if self.Department == correctdept : 
            
            ##Add logic to only accept barcoded shelf for Hold Area 1 or 2. Do not accept Hold Area1 as correct for example
            
            ##Hold Area 1, 2, VLM have their own special rules for barcode acceptance, etc.
            ##For example, VLM accepts VLM but then changes global rank in Visual to 200
            if self.Department == correctdept \
                and correctdept != 'HOLD AREA1' \
                and correctdept != 'HOLD AREA2' \
                and correctdept != 'VLM' : 
                self.AllowedDepts = "None" #Allowed Departments is allowed departments other than correct department
                DepartmentLog.setArrival(self, LotCount)
                
            ##Add 06/05/19 for Counting override##
            ##Moved 06/14/19 ##
            ###This needs to be before alternates so that it takes precedence##
            ###If someone is delivering to counting, it does not matter where the succeeding
            ###step says to take the job.  Counting is always an intermediary step before next operation
            elif correctdept in ALL_PORTS and self.Department in COUNTING_LIST:
                DepartmentLog.buildAllowedDeptsList(self, COUNTING_LIST)
                
                DepartmentLog.setArrival(self, LotCount)
                DepartmentLog.setNote(self, LotCount, "FOR COUNTING")                
                

            elif correctdept == "POINT":
                DepartmentLog.buildAllowedDeptsList(self, POINT_LIST)
                if self.Department in POINT_LIST:
                    DepartmentLog.setArrival(self, LotCount)
                else:
#                print("oops")
                    self.WrongLocation = True 
                    
            elif correctdept == "HEAD FORM":       
                DepartmentLog.buildAllowedDeptsList(self, HEAD_FORM_LIST)
                if self.Department in HEAD_FORM_LIST:
                    DepartmentLog.setArrival(self, LotCount)
                else:
#                print("oops")
                    self.WrongLocation = True  
                    
            elif correctdept == "WASHING STATION":       
                DepartmentLog.buildAllowedDeptsList(self, WASHING_LIST)
                if self.Department in WASHING_LIST:
                    DepartmentLog.setArrival(self, LotCount) 
                else:
#                print("oops")
                    self.WrongLocation = True 
                    
            elif correctdept == "DIMENSIONAL INSPECTION":       
                DepartmentLog.buildAllowedDeptsList(self, DIMENSIONAL_LIST)
                if self.Department in DIMENSIONAL_LIST:
                    DepartmentLog.setArrival(self, LotCount)                     
                else:
#                print("oops")
                    self.WrongLocation = True 
            elif correctdept == "VISUAL INSPECTION":       
                DepartmentLog.buildAllowedDeptsList(self, VISUAL_LIST)
                if self.Department in VISUAL_LIST:
                    DepartmentLog.setArrival(self, LotCount)   
                else:
#                print("oops")
                    self.WrongLocation = True 
                    
            elif correctdept == "CROSS DRILL DEBURR":       
                DepartmentLog.buildAllowedDeptsList(self, CROSSDRILL_LIST)
                if self.Department in CROSSDRILL_LIST:
                    DepartmentLog.setArrival(self, LotCount) 
                else:
#                print("oops")
                    self.WrongLocation = True 
            elif correctdept == "QUALITY ENGINEERING":       
                DepartmentLog.buildAllowedDeptsList(self, QUALITY_ENG_LIST)
                if self.Department in QUALITY_ENG_LIST:
                    DepartmentLog.setArrival(self, LotCount)  
                else:
#                print("oops")
                    self.WrongLocation = True                     
            elif correctdept == "THRU GRIND":       
                DepartmentLog.buildAllowedDeptsList(self, SLUG_GRIND_LIST)
                if self.Department in SLUG_GRIND_LIST:
                    DepartmentLog.setArrival(self, LotCount) 
                else:
#                print("oops")
                    self.WrongLocation = True 
            ## Added 01/24/19
            elif correctdept == "LUBE":       
                DepartmentLog.buildAllowedDeptsList(self, LUBE_LIST)
                if self.Department in LUBE_LIST:
                    DepartmentLog.setArrival(self, LotCount) 
                else:
#                print("oops")
                    self.WrongLocation = True   
            ## Added 04/03/19
            elif correctdept == "CUT OFF RADIAC":       
                DepartmentLog.buildAllowedDeptsList(self, RADIAC_LIST)
                if self.Department in RADIAC_LIST:
                    DepartmentLog.setArrival(self, LotCount) 
                else:
#                print("oops")
                    self.WrongLocation = True 

            ## Added 04/03/19
            elif correctdept == "THREAD ROLL":       
                DepartmentLog.buildAllowedDeptsList(self, THREAD_ROLL_LIST)
                if self.Department in THREAD_ROLL_LIST:
                    DepartmentLog.setArrival(self, LotCount) 
                else:
#                print("oops")
                    self.WrongLocation = True 
            ## Added 04/03/19
            elif correctdept == "FILLET ROLL":       
                DepartmentLog.buildAllowedDeptsList(self, FILLET_ROLL_LIST)
                if self.Department in FILLET_ROLL_LIST:
                    DepartmentLog.setArrival(self, LotCount)
                else:
#                print("oops")
                    self.WrongLocation = True    
                    
#            ##/7/22/19 for VLM machine logic
#            elif correctdept == VLM_HOLD_AREA:       
#                DepartmentLog.buildAllowedDeptsList(self, VLM_LIST)
#                if self.Department in VLM_LIST:
#                    DepartmentLog.setArrival(self, LotCount)
#                else:
##                print("oops")
#                    self.WrongLocation = True              
                    
                    
                    
	    ## ADded 06/26/19 for a special Hardness Test operation 
            elif correctdept == "LAB":       
                DepartmentLog.buildAllowedDeptsList(self, LAB_LIST)
                if self.Department in LAB_LIST:
                    DepartmentLog.setArrival(self, LotCount) 



                else:
#                print("oops")
                    self.WrongLocation = True 
                    

                
                    
                    
        ### HOLD AREAS   
            elif correctdept == MAIN_HOLD_AREA:       
#                self.AllowedDepts = "100 thru 155, 169 thru 175"
                self.AllowedDepts = "100 thru 155"

                if self.Department in MAIN_HOLD_AREA_LIST:
                    DepartmentLog.holdAreaAction(self, self.Department, cursor, cnxn, LotCount, base, lot, split)
                else:
#                print("oops")
                    self.WrongLocation = True 
            
            elif correctdept == ROUGH_GRIND_AREA:       
#                self.AllowedDepts = "100 thru 155, 169 thru 175"
                self.AllowedDepts = "156-161, 143-148, 137-142, 175-180"

                if self.Department in ROUGH_GRIND_AREA_LIST:
                    DepartmentLog.holdAreaAction(self, self.Department, cursor, cnxn, LotCount, base, lot, split)
                else:
#                print("oops")
                    self.WrongLocation = True   
                    
            elif correctdept == FINISH_GRIND_AREA:       
#                self.AllowedDepts = "100 thru 155, 169 thru 175"
                self.AllowedDepts = "169-174, 162-167"

                if self.Department in FINISH_GRIND_AREA_LIST:
                    DepartmentLog.holdAreaAction(self, self.Department, cursor, cnxn, LotCount, base, lot, split)
                else:
#                print("oops")
                    self.WrongLocation = True                   
                
                
                #Obsolte 7-24-19
#            elif correctdept == GRIND_HOLD_AREA:       
#                self.AllowedDepts = "155 thru 168"
#
#
#                if self.Department in GRIND_HOLD_AREA_LIST:
#                    DepartmentLog.holdAreaAction(self, self.Department, cursor, cnxn, LotCount, base, lot, split) 
#                else:
##                print("oops")
#                    self.WrongLocation = True    
#                ##DEFAULT CASE  
            elif correctdept == VLM_HOLD_AREA:
                self.AllowedDepts = "VLM"
                
                if self.Department in VLM_HOLD_AREA_LIST:
#                    self.Department = 200 #
                    
                    ##Pass 200 into the department which will then update global rank
                    DepartmentLog.holdAreaAction(self, '200', cursor, cnxn, LotCount, base, lot, split) 
                else:
#                print("oops")
                    self.WrongLocation = True   

            
            
            else:
#                print("oops")
                self.WrongLocation = True      
                    
                    
#            ## Allow pointing traub to go to POINT (but not vice versa)
#            elif self.Department in POINT_LIST and correctdept == "POINT":
#                DepartmentLog.setArrival(self, LotCount)

                
            ## Allow head form list to check in to HEAD FORM instead
#            elif self.Department in HEAD_FORM_LIST and correctdept == "HEAD FORM":
#                DepartmentLog.setArrival(self, LotCount)
#                    
                
            ##If washing station is next, but HT, fillet, passivation, thread roll follows
            ## users take directly to HT, fillet... instead of washing. Allow check in at following location.
                
#            elif self.Department in WASHING_LIST and correctdept == "WASHING STATION":
#                DepartmentLog.setArrival(self, LotCount)

#                
#            elif self.Department in DIMENSIONAL_LIST and correctdept == "DIMENSIONAL INSPECTION":
#                DepartmentLog.setArrival(self, LotCount)
#                self.AllowedDepts = DIMENSIONAL_LIST

#            elif self.Department in VISUAL_LIST and correctdept == "VISUAL INSPECTION":
#                DepartmentLog.setArrival(self, LotCount)
#                self.AllowedDepts = VISUAL_LIST

#            elif self.Department in CROSSDRILL_LIST and correctdept == "CROSS DRILL DEBURR":
#                DepartmentLog.setArrival(self, LotCount)
#                self.AllowedDepts = CROSSDRILL_LIST

#            elif self.Department in QUALITY_ENG_LIST and correctdept == "QUALITY ENGINEERING":
#                DepartmentLog.setArrival(self, LotCount)
#                self.AllowedDepts = QUALITY_ENG_LIST

#
#            elif self.Department in SLUG_GRIND_LIST and correctdept == "THRU GRIND":
#                DepartmentLog.setArrival(self, LotCount)
#                self.AllowedDepts = SLUG_GRIND_LIST


            ##If correct department should be hold area1 check to see if department
            ##logged is in MAIN_HOLD_AREA_LIST (100... etc 155)
#            elif self.Department in MAIN_HOLD_AREA_LIST and correctdept == MAIN_HOLD_AREA:
#                DepartmentLog.holdAreaAction(self, cursor, cnxn, LotCount, base, lot, split)
##                print("1111")
                
            ## If correct department should be GRIND HOLD AREA / HOLD AREA 2
            ## IT can be clocked in to MAIN HOLD AREA per Luc Villemin 11/2/18
            ## But NOT Vice Versa, MAIN cannot go to ROUGH hold area
#            elif self.Department in MAIN_HOLD_AREA_LIST and correctdept == GRIND_HOLD_AREA: 
##                print("2222")
#                DepartmentLog.holdAreaAction(self, cursor, cnxn, LotCount, base, lot, split)

#                
#            elif self.Department in GRIND_HOLD_AREA_LIST and correctdept == GRIND_HOLD_AREA:
##                print("@@@@@")
#                DepartmentLog.holdAreaAction(self, cursor, cnxn, LotCount, base, lot, split)





	#cnxn.close() #Warning this breaks the django server. I don't know why.
        super(DepartmentLog, self).save(*args, **kwargs)
	
    
    def __str__(self):
        return "DepartmentLog: {}".format(self.LotNo)
    
    
#    def holdAreaAction(self, cursor, cnxn, lotcount, base, lot, split):
##        print("hold area ction")
##        print("self dept", self.Department)
#        CountLog.GlobalRank = self.Department
##        cursor.execute("UPDATE WORK_ORDER SET GLOBAL_RANK = ? WHERE BASE_ID = ? AND LOT_ID = ? AND SPLIT_ID = ? ",(self.Department, base,lot,split,))
#        DepartmentLog.updateVisualRank(cursor, cnxn, self.Department, base, lot, split)
##        cursor.execute("UPDATE WO_SCH_PRIORITY SET GLOBAL_RANK = ? WHERE SCHEDULE_ID = ? and WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ? ", (self.Department, "STANDARD", base, lot, split,) )
# 
##        cnxn.commit()
#        
#        DepartmentLog.setArrival(self, lotcount)
        
    ##Check if a string represents an integer, such as department global rank
    def RepresentsInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    
    def holdAreaAction(self, department, cursor, cnxn, lotcount, base, lot, split):
#        print("hold area ction")
#        print("self dept", self.Department)
#        CountLog.GlobalRank = self.Department
        
        ##department is globalrank in this case, I.E. location 
        print("department: ", department)
        print("typedept: ", type(department))

        
        ##Check if department is an int or can be converted to int, if yes then proceed
        ##I.E. do not assign global rank to a non-int value or str(int) version of that value
        if(DepartmentLog.RepresentsInt(department)):
            if(self.DeptGlobalRank >19):
                CountLog.GlobalRank = department
    #        cursor.execute("UPDATE WORK_ORDER SET GLOBAL_RANK = ? WHERE BASE_ID = ? AND LOT_ID = ? AND SPLIT_ID = ? ",(self.Department, base,lot,split,))
            DepartmentLog.updateVisualRank(self, cursor, cnxn, department, base, lot, split)
    #        cursor.execute("UPDATE WO_SCH_PRIORITY SET GLOBAL_RANK = ? WHERE SCHEDULE_ID = ? and WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ? ", (self.Department, "STANDARD", base, lot, split,) )
#            print("yes isinstance")
        else:
            CountLog.GlobalRank = 999
#            print("no isinstance")
        
 
#        cnxn.commit()
        
        DepartmentLog.setArrival(self, lotcount)    
    
        
    def updateVisualRank(self, cursor, cnxn, globalrank, base, lot, split):
        
        ##VLM (rank 200) has to initially be >30 to pass test in CountingLog
        ##so jobs that go to VLM have to be >30 
        
        
        if(self.DeptGlobalRank >19):
            try:
                cursor.execute("UPDATE WO_SCH_PRIORITY SET GLOBAL_RANK = ? WHERE SCHEDULE_ID = ? and WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ? ", (globalrank, "STANDARD", base, lot, split,) )
                cnxn.commit()        
            except Exception as ex:
                print("error: ", ex)
    #        cnxn.commit()        
        else:
            print("do nothing! rank <=19")
#            a = 1
#            ###Do nothing for now
#            ## in the future it might be work doing something with notes?

    '''Flag the CountLog model that DepartmentLog model has received the count in port of entry'''
    def setArrival(self, lotcount):
        lotcount.ArrivedTo = True
        lotcount.save()
        self.WrongLocation = False #Should be redundant code 
    
    ''' Set a note in the CountLog model during the Department Log log in operation'''
    def setNote(self, lotcount, note):
        if lotcount.Notes is None:
            lotcount.Notes = note
        else:
            lotcount.Notes = lotcount.Notes +" " + note
        
        
        print("lotcount.Notes: ", lotcount.Notes)
        lotcount.save()
    
    '''Build allowed alternate departments for show in Department Log report of MSAPP'''
    def buildAllowedDeptsList(self, LIST):
        ##Default is string "None", if it is this, override the default value of None when adding.
        if (self.AllowedDepts == "None"):
            self.AllowedDepts = ""
            
        for x in LIST:
            try:
                self.AllowedDepts += str(x+" ")
            except TypeError:
                self.AllowedDepts = str(x +" ")
                
class DepartmentLogUsers(models.Model):
    listNumber = models.IntegerField(unique = True)
    userName = models.CharField(max_length = 100)
    userActive = models.BooleanField(default = True)
    
    def __str__(self):
        return str(self.listNumber) +" - " + str(self.userName)
    
        
        