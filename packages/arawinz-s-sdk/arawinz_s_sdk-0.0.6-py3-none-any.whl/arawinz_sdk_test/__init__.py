import requests

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.logic import get_application_address
from pytz import timezone
import datetime

algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)
params = algod_client.suggested_params()


class ArawinzSdk:

    def __init__(self):
        pass

    def deploy(owner_passphrase,org_name,org_Email):
        owner = mnemonic.to_public_key(owner_passphrase)
        private_key = mnemonic.to_private_key(owner_passphrase)

        local_ints = 0
        local_bytes = 11
        global_ints = 0
        global_bytes = 3
        global_schema = transaction.StateSchema(global_ints, global_bytes)
        local_schema = transaction.StateSchema(local_ints, local_bytes)

        

        approval_teal= b'\x06 \x01\x01&\x0c\x05owner\x07Manager\x08Password\x08check_in\tcheck_out\x03POE\x03POL\x05Leave\x04Name\x05Email\x0bDesignation\x06Mobile1\x18\x81\x00\x12@\x03P1\x19\x81\x04\x12@\x03@1\x19\x81\x05\x12@\x0301\x19"\x12@\x03\'6\x1a\x00\x80\x10setting_managers\x12@\x02\xa96\x1a\x00\x80\x0ecreate_employe\x12@\x02*6\x1a\x00\x80\x0fupdate_password\x12@\x01\xfc6\x1a\x00\x80\x0bApply_leave\x12@\x01\xc26\x1a\x00\x80\rApprove_leave\x12@\x01}6\x1a\x00\x80\tApply_POL\x12@\x01G6\x1a\x00\x80\x0bApprove_POL\x12@\x01\t6\x1a\x00\x80\tApply_POE\x12@\x00\xd36\x1a\x00\x80\x0bApprove_POE\x12@\x00\x956\x1a\x00+\x12@\x00j6\x1a\x00\'\x04\x12@\x0076\x1a\x00\x80\x06log_in\x12@\x00\x1c6\x1a\x00\x80\norg_log_in\x12@\x00\x01\x001\x00(d\x12D"C1\x00*b6\x1a\x01\x01\x12D"C1\x00\'\x046\x1a\x01f\x80\x11employee_checkout\xb01\x00\xb01\x00+b\xb06\x1a\x01\xb0"C1\x00+6\x1a\x01f\x80\x10employee_checkin\xb01\x00\xb06\x1a\x01\xb0"C1\x00(d\x12D6\x1c\x01\'\x056\x1a\x01f\x80\x0bpoe_approve\xb01\x00\xb06\x1c\x01\xb06\x1a\x01\xb0"C1\x00\'\x056\x1a\x01f\x80\x0bpoe_request\xb01\x00)b\xb01\x00\xb06\x1a\x01\xb0"C1\x00(d\x12D6\x1c\x01\'\x066\x1a\x01f\x80\x0bpol_approve\xb01\x00\xb06\x1c\x01\xb06\x1a\x01\xb0"C1\x00\'\x066\x1a\x01f\x80\x0bpol_request\xb01\x00)b\xb01\x00\xb06\x1a\x01\xb0"C1\x006\x1c\x01)b\x12D6\x1c\x01\'\x076\x1a\x01f\x80\rleave_approve\xb01\x00\xb06\x1c\x01\xb06\x1a\x01\xb0"C1\x00\'\x076\x1a\x01f\x80\rleave_request\xb01\x00)b\xb01\x00\xb06\x1a\x01\xb0"C6\x1c\x01*b6\x1a\x01\x01\x12D6\x1c\x01*6\x1a\x02\x01f"C1\x00(d\x12D6\x1c\x01\'\x086\x1a\x01f6\x1c\x01\'\t6\x1a\x02f6\x1c\x01\'\n6\x1a\x03f6\x1c\x01*6\x1a\x04\x01f6\x1c\x01\'\x0b6\x1a\x05f6\x1c\x01)6\x1c\x02f\x80\x10employee_created\xb06\x1c\x02\xb06\x1c\x01\xb06\x1a\x01\xb06\x1a\x02\xb06\x1a\x03\xb06\x1a\x05\xb0"C1\x00(d\x12D6\x1c\x01\'\x086\x1a\x01f6\x1c\x01\'\t6\x1a\x02f6\x1c\x01\'\n6\x1a\x03f6\x1c\x01*6\x1a\x04\x01f6\x1c\x01\'\x0b6\x1a\x05f6\x1c\x01)2\tf\x80\x0fmanager_created\xb02\t\xb06\x1c\x01\xb06\x1a\x01\xb06\x1a\x02\xb06\x1a\x03\xb06\x1a\x05\xb0"C"C1\x00(d\x12D"C1\x00(d\x12D"C(2\tg\x80\x08org_name6\x1a\x00g\x80\torg_email6\x1a\x01g"C'

        clear_teal = b'\x06\x81\x00C'
        on_complete = transaction.OnComplete.NoOpOC.real

        txn = transaction.ApplicationCreateTxn(
            owner,
            params,
            on_complete,
            approval_teal,
            clear_teal,
            global_schema,
            local_schema,
            app_args=[org_name,org_Email]
            )

        # sign transaction
        signed_txn = txn.sign(private_key)
        tx_id = signed_txn.transaction.get_txid()

        # send transaction
        algod_client.send_transactions([signed_txn])

        # wait for confirmation
        try:
            transaction_response = transaction.wait_for_confirmation(algod_client, tx_id, 4)
            print("TXID: ", tx_id)
            print("Result confirmed in round: {}".format(transaction_response['confirmed-round']))
            # return {"status":True,''}
        except Exception as err:
            print(err)
            return {'status':False}

        # display results
        transaction_response = algod_client.pending_transaction_info(tx_id)
        app_id = transaction_response['application-index']
        Contract_Address = get_application_address(app_id)
        print("Created new app-id:", app_id)
        print("SC Address: ",get_application_address(app_id))
        print("----------------------------Application Deployed----------------------------")
        return {'status':True,'sc_add':Contract_Address,'owner_add':owner,'app_id':app_id}

     



    def feeding_contract(self, owner_passphrase,receiver):
        owner = mnemonic.to_public_key(owner_passphrase)
        private_key = mnemonic.to_private_key(owner_passphrase)
        note = "Algos".encode()
        # print("----------------------------Feeding Application----------------------------")
        print("My address: {}".format(owner))
        account_info = algod_client.account_info(owner)
        amount = 4000000
        
        unsigned_txn = transaction.PaymentTxn(owner, params, receiver,amount,None,note)

        # sign transaction
        signed_txn = unsigned_txn.sign(private_key)

        # submit transaction
        txid = algod_client.send_transaction(signed_txn)
        print("Signed transaction with txID: {}".format(txid))

        # wait for confirmation 
        try:
            confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 20)  
        except Exception as err:
            print(err)
            return False
        print("Starting Account balance: {} Algos".format(account_info.get('amount') / 1000000))
        print("Amount transfered: {} Algos".format((amount)/1000000))

        account_info = algod_client.account_info(owner)
        print("Final Account balance: {} Algos".format(account_info.get('amount') / 1000000))
        print("----------------------------Application Feeded----------------------------")
        return True

    def App_optin(self,app_id,passphrase):
        # declare sender
        private_key = mnemonic.to_private_key(passphrase)
        sender = account.address_from_private_key(private_key)
        
        print("OptIn from account: ", sender)

        
        # create unsigned transaction
        txn = transaction.ApplicationOptInTxn(sender, params, app_id)
        # sign transaction
        signed_txn = txn.sign(private_key)
        
        try:    
            tx_id = signed_txn.transaction.get_txid()
            # send transaction
            tx_id = algod_client.send_transactions([signed_txn])
            # await confirmation
            transaction.wait_for_confirmation(algod_client, tx_id,20)
            # display results
            transaction_response = algod_client.pending_transaction_info(tx_id)
            print("Opted to App ID:", transaction_response["txn"]["txn"]["apid"])
            
        except Exception as err:
            print(type(err))
            return False
        return True

    def set_manager01(self,app_id,owner_passphrase,m_addr,name,email,designation,password,mobile):
        owner = mnemonic.to_public_key(owner_passphrase)
        private_key = mnemonic.to_private_key(owner_passphrase)
        params = algod_client.suggested_params()
        print("Setting",m_addr, "as a Manager:")
        # create unsigned transaction
        txn = transaction.ApplicationNoOpTxn(
            owner,
            params,
            index=app_id,
            app_args=["setting_managers",name,self.__EmailEncode(email),designation,password,self.__mobileEncode(mobile)],
            accounts=[m_addr]
        )
        # sign transaction
        signed_txn = txn.sign(private_key)
        try:
            tx_id = signed_txn.transaction.get_txid()
            # send transaction
            tx_id =algod_client.send_transactions([signed_txn])
            # await confirmation
            transaction.wait_for_confirmation(algod_client, tx_id,20)
            # display results
            print("Manager set")
        except Exception as err:
            print(err)
            return False
        return True

    def create_employee(self, app_id,owner_passphrase,employee_addr,manager_addr,name,email,designation,password,mobile):
        owner = mnemonic.to_public_key(owner_passphrase)
        private_key = mnemonic.to_private_key(owner_passphrase)
        params = algod_client.suggested_params()
        print("Creating", employee_addr,"as a Employee")  

        txn = transaction.ApplicationNoOpTxn(
            owner,
            params,
            index=app_id,
            app_args=["create_employe",name,self.__EmailEncode(email),designation,password,self.__mobileEncode(mobile)],
            accounts=[employee_addr,manager_addr]
        )

        signed_txn = txn.sign(private_key)

        try:
            tx_id = signed_txn.transaction.get_txid()
            tx_id =algod_client.send_transactions([signed_txn])
            transaction.wait_for_confirmation(algod_client, tx_id,20)

            # display results
            print("Employee created")
        except Exception as err:
            print(err)
            return False
        print("----------------------------------------------------")
        return True

    def createWallet(self, owner_passphrase,app_id,name, email,designation,password, mobile,manager):
        
        private_key, address = account.generate_account()
        print("Wallet address: {}".format(address))
        print("Wallet private key: {}".format(private_key))
        print("Wallet passphrase: {}".format(mnemonic.from_private_key(private_key)))
        feed =  self.feeding_contract(owner_passphrase,address)
        
        if feed:
            optin = self.App_optin(app_id,mnemonic.from_private_key(private_key))
            if optin:
                if manager=='SC':
                    status = self.set_manager01(app_id,owner_passphrase,address,name, email,designation,password, mobile)
                    if status:
                        return {'status':True,'wallet_address':address,'wallet_passphrase':mnemonic.from_private_key(private_key)}
                    else:
                        return {'status':False,"msg":"Failed to Created Manager's Local Storage"}
                else:
                    status = self.create_employee(app_id,owner_passphrase,address,manager,name,email,designation,password,mobile)
                    if status:
                        return {'status':True, 'wallet_address':address,'wallet_passphrase':mnemonic.from_private_key(private_key)}
                    else:
                        return {'status':False,"msg":"Failed to Created Manager's Local Storage"}
            return {'status':False,"msg":"OPTIN to Smart Contract Failed"}
        else:
            return {'status':False,"msg":"unable to feed the Given Wallet Address"}


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
