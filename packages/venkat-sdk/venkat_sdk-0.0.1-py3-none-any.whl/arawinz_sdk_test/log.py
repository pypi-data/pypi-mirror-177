import requests
from algosdk.v2client import algod
from pytz import timezone
import base64
import algosdk
import datetime

algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)
params = algod_client.suggested_params()

class FetchData:

    def __init__(self):
        pass


    ####  COMMON START  ####
    def __getDateTime(self):
        now = datetime.datetime.now(timezone('Asia/Kolkata'))
        datetimeee=datetime.datetime(now.year, now.month, now.day,now.hour,now.minute,now.second)
        datetimee=str(datetimeee)
        return datetimee

    def __getDateOnly(self):
        now = datetime.datetime.now(timezone('Asia/Kolkata'))
        datetimeee=datetime.datetime(now.year, now.month, now.day,now.hour,now.minute)
        datetimee=str(datetimeee)
        return datetimee.split(" ")[0]



####  COMMON END  ####

    def __read_local_state(self, app_id, addr) :  
        results = algod_client.account_info(addr)
        local_states = results['apps-local-state']
        # print(local_states[app_id])
        localdata=[]
        for localstate in local_states:
            if localstate['id']== app_id:
                localdata=localstate['key-value']
        # print(localdata)
        arr={}
        for data in localdata:
            if str(base64.b64decode(data['key']),"UTF-8")=='Name':
                arr['name']=str(base64.b64decode(data['value']['bytes']),"UTF-8")
            if str(base64.b64decode(data['key']),"UTF-8")=='Email':
                arr['email']=(str(base64.b64decode(data['value']['bytes']),"UTF-8"))
            if str(base64.b64decode(data['key']),"UTF-8")=='Designation':
                arr['designation']=str(base64.b64decode(data['value']['bytes']),"UTF-8")
            if str(base64.b64decode(data['key']),"UTF-8")=='Mobile':
                arr['mobile']=(str(base64.b64decode(data['value']['bytes']),"UTF-8"))
        # print(arr)
        return arr   


    def __getHoursDiff(self,checkIn,checkOut):
        format_data = "%Y-%m-%d %H:%M:%S"
        checkInTime = datetime.strptime(checkIn, format_data)
        checkOutTime = datetime.strptime(checkOut, format_data)
        diff = checkOutTime - checkInTime
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        total = float(hours)+(float(minutes)/100)
        return total




        ## GET ONLY MANAGER's DATA in an ORG

    def getAllManagers(self,app_id):
        managers = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'manager_created':
                    arr = {
                            'org_address': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'name':str(base64.b64decode(logdata[3]),"UTF-8"),
                            'email':(str(base64.b64decode(logdata[4]),"UTF-8")),
                            'designation':str(base64.b64decode(logdata[5]),"UTF-8"),
                            'mobile':(str(base64.b64decode(logdata[6]),"UTF-8")),

                    }
                    managers.append(arr)
        return managers


    def getAllEmployees(self,app_id):
        employees = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'employee_created':
                    arr = {
                        'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                        'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                        'name':str(base64.b64decode(logdata[3]),"UTF-8"),
                        'email':(str(base64.b64decode(logdata[4]),"UTF-8")),
                        'designation':str(base64.b64decode(logdata[5]),"UTF-8"),
                        'mobile':(str(base64.b64decode(logdata[6]),"UTF-8")),

                    }
                    employees.append(arr)
        return employees


    def getAllEmployeesUnderManager(self,app_id,manager):
        employees = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'employee_created':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==manager:
                        arr = {
                            'manager': manager,
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'name':str(base64.b64decode(logdata[3]),"UTF-8"),
                            'email':(str(base64.b64decode(logdata[4]),"UTF-8")),
                            'designation':str(base64.b64decode(logdata[5]),"UTF-8"),
                            'mobile':(str(base64.b64decode(logdata[6]),"UTF-8")),

                        }
                        employees.append(arr)
        return employees


    
    def dailyAttendence(self,app_id):
        attendence = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:        
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'employee_checkout':
                    workingHours = self.__getHoursDiff(str(base64.b64decode(logdata[2]),"UTF-8"),str(base64.b64decode(logdata[3]),"UTF-8"))
                    arr = {
                        # 'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                        'address':algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                        'checkInTime':str(base64.b64decode(logdata[2]),"UTF-8"),
                        'checkOutTime':str(base64.b64decode(logdata[3]),"UTF-8"),
                        "workingHours":workingHours
                    }
                    attendence.append(arr)
        return attendence
             

    def dailyAttendenceOfEmployee(self,app_id, employee):
        attendence = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:        
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'employee_checkout':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==employee:
                        workingHours = self.__getHoursDiff(str(base64.b64decode(logdata[2]),"UTF-8"),str(base64.b64decode(logdata[3]),"UTF-8"))
                        arr = {
                            # 'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'checkInTime':str(base64.b64decode(logdata[2]),"UTF-8"),
                            'checkOutTime':str(base64.b64decode(logdata[3]),"UTF-8"),
                            "workingHours":workingHours   
                        }
                        attendence.append(arr)
        return attendence
   


    ## get ALL LEAVE REQUESTS DATA IN AN ORG
    def getAllLeaveRequests(self,app_id):
        lr = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'leave_request':
                    common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                    arr = {
                        'name':common_data['name'],
                        'email':common_data['email'],
                        'mobile':common_data['mobile'],
                        'designation':common_data['designation'],
                        'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                        'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                        'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                    }
                    lr.append(arr)
        # print(lr)
        return lr

    ### GET EMPLOYEE's LEAVE REQUEST DATA

    def getLeaveRequestsOfEmployee(self,app_id,EMP_Address):
        lr_for_emp = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'leave_request':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==EMP_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                            'name':common_data['name'],
                            'email':common_data['email'],
                            'mobile':common_data['mobile'],
                            'designation':common_data['designation'],
                            'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        lr_for_emp.append(arr)
        # print(lr_for_emp)
        return lr_for_emp
        

     ### GET EMPLOYEE'S LEAVE REQUEST DATA BY MANAGER ADD

    def getLeaveRequestsByManager(self,app_id,M_Address):
        lr = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'leave_request':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==M_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        lr.append(arr)
        return lr


    ## GET ALL LEAVE APPROVALS DATA 

    def getAllLeaveApprovals(self,app_id):
        la = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'leave_approve':
                    common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                    arr = {
                            'name':common_data['name'],
                            'email':common_data['email'],
                            'mobile':common_data['mobile'],
                            'designation':common_data['designation'],
                            'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                    }
                    la.append(arr)
        return la

    ## GET LEAVE APPROVAL DATA BY EMPLOYEE ADDRESS

    def getLeaveApprovalsOfEmployee(self,app_id,EMP_Address):
        la = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'leave_approve':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==EMP_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        la.append(arr)
        return la


    ### GET EMPLOYEE LEAVE REQUESTS BY MANAGER   (change title and Method name)

    def getLeaveApprovalsByManager(self,app_id,M_Address):
        la = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'leave_approve':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==M_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        la.append(arr)
        return la



    ## GET ALL PROOF OF LEARNING REQUESTS


    def getAllPOLRequests(self,app_id):
        polr_e = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'pol_request':    
                    common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                    arr = {
                            'name':common_data['name'],
                            'email':common_data['email'],
                            'mobile':common_data['mobile'],
                            'designation':common_data['designation'],
                            'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                    }
                    polr_e.append(arr)
        return polr_e

        ## GET ALL PROOF OF LEARNING REQUESTS by Manager



    ## GET ALL PROOF OF LEARNING APPROVED DATA by EMPLOYEE

    def getAllPOLRequestsEMP(self,app_id,EMP_Address):
        polr_e = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'pol_request':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==EMP_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        polr_e.append(arr)
        return polr_e


    def getAllPOLReqDataByManager(self,app_id,M_Address):
        polr_m = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'pol_request':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==M_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        polr_m.append(arr)
        return polr_m

        ## GET ALL PROOF OF LEARNING APPROVED DATA

    def getAllPOLAppData(self,app_id):
        pola_owner = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'pol_approve':
                    common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                    arr = {
                            'name':common_data['name'],
                            'email':common_data['email'],
                            'mobile':common_data['mobile'],
                            'designation':common_data['designation'],
                            'owner': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                    }
                    pola_owner.append(arr)
        return pola_owner



        ## GET ALL PROOF OF LEARNING APPROVED DATA BY EMPLOYEE ADDRESS

    def getAllPOLAppDataByEMP(self,app_id,EMP_Address):
        pola_e = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'pol_approve':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==EMP_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        pola_e.append(arr)
        return pola_e


        ## GET ALL PROOF OF LEARNING APPROVED DATA BY OWNER / COMPANY ADDRESS
    def getAllPOLAppDataByOwner(self,app_id,owner_Address):
        pola_owner = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'pol_approve':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==owner_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'owner': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        pola_owner.append(arr)
        return pola_owner

    
        ## GET ALL PROOF OF EXPERIENCE REQUESTS
    def getAllProofOfExpReqs(self,app_id):
        poer_employee = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'poe_request':
                    common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                    arr = {
                            'name':common_data['name'],
                            'email':common_data['email'],
                            'mobile':common_data['mobile'],
                            'designation':common_data['designation'],
                            'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                    }
                    poer_employee.append(arr)
        return poer_employee



    ## GET ALL PROOF OF EXPERIENCE REQUESTS BY EMPLOYEE


    def getProofOfExpReqByEmployee(self,app_id,EMP_Address):
        poer_employee = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'poe_request':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==EMP_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        poer_employee.append(arr)
        return poer_employee




    ## GET ALL PROOF OF EXPERIENCE REQUESTS BY MANAGER

    def getAllProofOfExpReqByManager(self,app_id,M_Address):
        poer_manager = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'poe_request':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==M_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        poer_manager.append(arr)
        return poer_manager



    ## GET ALL PROOF OF EXPERIENCE APPROVALS

    def getAllProofOfExperienceApproved(self,app_id):
        poea_employee = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'poe_approve':
                    common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                    arr = {
                            'name':common_data['name'],
                            'email':common_data['email'],
                            'mobile':common_data['mobile'],
                            'designation':common_data['designation'],
                            'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                            'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                            'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                    }
                    poea_employee.append(arr)
        return poea_employee


    ###   GET EMPLOYEE PROOF OF EXPERIENCE APPROVAL BY EMPLOYEE ADDRESS

    def getEmployeeProofOfExperienceApprovalsOfEmployee(self,app_id,EMP_Address):
        poea_employee = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'poe_approve':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==EMP_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        poea_employee.append(arr)
        return poea_employee


    ###   GET EMPLOYEE PROOF OF EXPERIENCE APPROVAL BY OWNER / COMPANY ADDRESS

    def getEmployeeProofOfExperienceApprovalsByOwner(self,app_id,owner_Address):
        poea_owner = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'poe_approve':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[1]))==owner_Address:
                        common_data= self.__read_local_state(algosdk.encoding.encode_address(base64.b64decode(logdata[2])),app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                'details':(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        poea_owner.append(arr)
        return poea_owner



    def read_local_state(self, addr, app_id) :  
        results = algod_client.account_info(addr)
        local_states = results['apps-local-state']
        # print(local_states[app_id])
        localdata=[]
        for localstate in local_states:
            if localstate['id']== app_id:
                localdata=localstate['key-value']
        # print(localdata)
        arr={}
        for data in localdata:
            if str(base64.b64decode(data['key']),"UTF-8")=='Name':
                arr['name']=str(base64.b64decode(data['value']['bytes']),"UTF-8")
            if str(base64.b64decode(data['key']),"UTF-8")=='Email':
                arr['email']=(str(base64.b64decode(data['value']['bytes']),"UTF-8"))
            if str(base64.b64decode(data['key']),"UTF-8")=='Designation':
                arr['designation']=str(base64.b64decode(data['value']['bytes']),"UTF-8")
            if str(base64.b64decode(data['key']),"UTF-8")=='Mobile':
                arr['mobile']=(str(base64.b64decode(data['value']['bytes']),"UTF-8"))
        # print(arr)
        return arr