import requests

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.logic import get_application_address
from pytz import timezone

algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)
params = algod_client.suggested_params()


class ArawinzSdk:

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

    def createWallet():
        private_key, address = account.generate_account()
        return {'wallet_address':address,'pass_phrase':mnemonic.from_private_key(private_key)}

# def createWallet():
#     Headers = { "tkn" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJIZWxsbyBmcm9tIFB1bGFyaXMifQ.jG9p7WQyIW581g_cAph4pQ0KbG6mPjl9QZsFgmoIyzY" }
#     url = "https://blockchain.nowigence.ai/create_wallet"
#     data = requests.get(url, headers=Headers)
#     data = data.json()
#     return data

# def createWalletNew():
#     Headers = { "tkn" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJIZWxsbyBmcm9tIFB1bGFyaXMifQ.jG9p7WQyIW581g_cAph4pQ0KbG6mPjl9QZsFgmoIyzY" }
#     url = "https://blockchain.nowigence.ai/create_wallet"
#     data = requests.get(url, headers=Headers)
#     data = data.json()
#     return data

# data = getData()

# print(data)