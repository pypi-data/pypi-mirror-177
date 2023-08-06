import requests
import base64
import algosdk
import json
from datetime import datetime
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.logic import get_application_address
from pytz import timezone

algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)




class Verify:

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


    def __EmailEncode(self,msg):
        msg = msg[::-1]
        msg=msg.replace("#", "%")
        msg=msg.replace("-", "?")
        msg=msg.replace("a", "^")
        msg=msg.replace("e", "&")
        msg=msg.replace("i", "~")
        msg=msg.replace("o", "_")
        msg=msg.replace("u", "+")
        return msg

    def __mobileEncode(self,msg):
        msg = msg[::-1]
        msg=msg.replace("1", "k")
        msg=msg.replace("2", "l")
        msg=msg.replace("3", "m")
        msg=msg.replace("4", "n")
        msg=msg.replace("5", "p")
        msg=msg.replace("6", "q")
        msg=msg.replace("7", "r")
        msg=msg.replace("8", "s")
        msg=msg.replace("9", "t")
        msg=msg.replace("0", "v")
        return msg

    def __EmailDecode(self,msg):
        msg = msg[::-1]
        msg=msg.replace("%", "#")
        msg=msg.replace("?", "-")
        msg=msg.replace( "^",'a')
        msg=msg.replace( "&",'e')
        msg=msg.replace( "~",'i')
        msg=msg.replace( "_",'o')
        msg=msg.replace( "+",'u')
        return msg

    def __mobileDecode(self,msg):
        msg = msg[::-1]
        msg=msg.replace("k","1")
        msg=msg.replace("l","2")
        msg=msg.replace("m","3")
        msg=msg.replace("n","4")
        msg=msg.replace("p","5")
        msg=msg.replace("q","6")
        msg=msg.replace("r","7")
        msg=msg.replace("s","8")
        msg=msg.replace("t","9")
        msg=msg.replace("v","0")
        return msg


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
                arr['email']=self.__EmailDecode(str(base64.b64decode(data['value']['bytes']),"UTF-8"))
            if str(base64.b64decode(data['key']),"UTF-8")=='Designation':
                arr['designation']=str(base64.b64decode(data['value']['bytes']),"UTF-8")
            if str(base64.b64decode(data['key']),"UTF-8")=='Mobile':
                arr['mobile']=self.__mobileDecode(str(base64.b64decode(data['value']['bytes']),"UTF-8"))
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

    def __verification_payment(self,verifier_passphrase,employee_address):
        sk = mnemonic.to_private_key(verifier_passphrase)
        sender = account.address_from_private_key(sk)
        account_info = algod_client.account_info(sender)
        # print("Account balance:{} microAlgos".format(account_info.get('amount')) +
        #       "\n")

        #build transaction"scan wheel heavy boy feature mind achieve crew comfort gauge valve crew assume doll pyramid insane toe tiger shed prevent color gown oil able inmate"
        params = algod_client.suggested_params()
        #comment out the next two line to use suggested fee
        params.flat_fee = True
        params.fee = 1000
        
        # receiver= employee_address
        #receiver = "SVIBHXXDWUFFCDTL2GXVFLFQJJNVA5OYKWRM2SPXY5OPTZTQXE7GCREXBA"

        txn =transaction.PaymentTxn(sender,params, employee_address, 2000000)

        #sign transaction
        signed_txn = txn.sign(sk)

        #submit transaction
        txid = algod_client.send_transaction(signed_txn)
        print("Successfully sent transaction with txID: {}".format(txid))

        #wait for confirmation
        try:
            confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
        except Exception as err:
            print(err)
            return False
        return True


####  COMMON END  ####


    ## Verify Proof of Learning
    def verify_proof_of_learning(self,app_id,verifier_passphrase,employee_address,subject):
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
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==employee_address:
                    # algosdk.encoding.encode_address(base64.b64decode(logdata[2]))
                        common_data= self.__read_local_state(employee_address,app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                # 'details':EmailDecode(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        pola_owner.append(arr)
        txt = self.__EmailDecode(str(base64.b64decode(logdata[3]),"UTF-8"))
        x = txt.split('#')
        if x[1] == subject:
            print(x)
            self.__verification_payment(verifier_passphrase,employee_address)
            return {'status':True,"proof_of_learning":"Available","details":x}
        else:
            return {'status':False,"proof_of_learning":"Not available / Not Verified"}
        #return pola_owner


    ## Verify Proof of Experience
    def verify_proof_of_experience(self,app_id,verifier_passphrase,employee_address,domain):
        pola_owner = []
        url=(f'https://testnet-idx.algonode.cloud/v2/transactions?application-id={app_id}')
        data = requests.get(url)
        data = data.json()
        transactions = data['transactions']
        for transaction in transactions:
            if 'logs' in transaction:
                logdata = transaction['logs']
                title = str(base64.b64decode(logdata[0]),"UTF-8")
                if title == 'poe_approve':
                    if algosdk.encoding.encode_address(base64.b64decode(logdata[2]))==employee_address:
                    # algosdk.encoding.encode_address(base64.b64decode(logdata[2]))
                        common_data= self.__read_local_state(employee_address,app_id)
                        arr = {
                                'name':common_data['name'],
                                'email':common_data['email'],
                                'mobile':common_data['mobile'],
                                'designation':common_data['designation'],
                                'manager': algosdk.encoding.encode_address(base64.b64decode(logdata[1])),
                                'address':algosdk.encoding.encode_address(base64.b64decode(logdata[2])),
                                # 'details':EmailDecode(str(base64.b64decode(logdata[3]),"UTF-8")),
                        }
                        pola_owner.append(arr)
        txt = self.__EmailDecode(str(base64.b64decode(logdata[3]),"UTF-8"))
        x = txt.split('#')
        if x[1] == domain:
            print(x)
            self.__verification_payment(verifier_passphrase,employee_address)
            return {'status':True,"proof_of_experience":"Available","details":x}
        else:
            print("experience not available")
            return {'status':False,"proof_of_experience":"Not available / Not Verified"}
        #return pola_owner

 