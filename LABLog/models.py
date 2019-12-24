from django.db import models

import pyodbc

# Create your models here.



### Update 1/22/19
### Race condition was present in checking of QLab open when multiple Q-LAB present. It would not always get the right one.
## Solution - check all, if any are open ,let users know which operations are open. Use OpNumOpen, add to model, with note on open operation number


##update Notes to blank = Trtue, remove print statements 1/23/19 CS

class LABLog(models.Model):

    Date = models.DateTimeField(auto_now = True)
    EmployeName = models.CharField(max_length=20)
    LotNo = models.CharField(max_length=20)
    Department = models.CharField(max_length=20,default='Q-LAB')
    VisualNotClosed = models.BooleanField(default = False)
    LabNotFinished = models.BooleanField(default = False)
    Notes = models.CharField(max_length = 800, blank = True, null = True)
    OpNumOpen = models.CharField(max_length = 100, null = True)
    
    
    def save(self,*args, **kwargs):
             
        if self.LotNo :
                        
            server = 'MSAVMFG1'
            database = 'VMLIVE'
            username = 'tastetf'
            password = 'Vi1234' 
            cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            cursor = cnxn.cursor()
            
            LotNo = self.LotNo
            
            base,lotsplit = LotNo.split("/")
            try :
                lot,split = lotsplit.split(".")
            except :  
                lot = lotsplit
                split = '0'
                
            cursor.execute("SELECT STATUS, SEQUENCE_NO FROM OPERATION WHERE WORKORDER_BASE_ID = ? AND WORKORDER_LOT_ID = ? AND WORKORDER_SPLIT_ID = ? AND RESOURCE_ID = ?",(base,lot,split,'Q-LAB',))
            STATUS = cursor.fetchall()
            
            self.OpNumOpen = ""
#            print("status: ", STATUS)
            for x in STATUS:
#                print("x: ", x)
                if (x[0] != 'C'):
                    
                    try:
                        self.OpNumOpen = self.OpNumOpen +" " + str(x[1])
#                        print(self.OpNumOpen)
                    except:
                        self.OpNumOpen = str(x[1])
#                        print(self.OpNumOpen)
                    self.VisualNotClosed = True
            
#            Status = str(STATUS[0])
#            if Status != 'C' : 
#                
#                self.VisualNotClosed = True 
                
        try : 
            cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM EMPLOYEE WHERE ID = ? ",(self.EmployeName,))
            EmpName = cursor.fetchone()
            
            name = str(str(EmpName[0])+"-"+str(EmpName[1]))
            
            self.EmployeName = name
            
        except : 

            self.EmployeName = self.EmployeName   
            
        cnxn.close()
        
        super(LABLog, self).save(*args, **kwargs)
    
    def __str__(self):
        return "DepartmentLog: {}".format(self.LotNo)