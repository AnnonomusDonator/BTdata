import sys
import requests
from bitcoin import *
import json

if(len(sys.argv) > 0):
    my_key1 = "c89e4494ddbca67b4d8eb6125de7def975aee12e4dcc8ffe19c98ef2c5dc03fa"
    my_key2 = "2ee7bdeabcb9854dd0ae3badbdbdaa2b1f46895da3f157b42ad1f7aa6df96d20"
    my_public_key1 = privtopub(my_key1)
    my_public_key2 = privtopub(my_key2)
    my_public_key3 = sys.argv[1]
    
    
    my_multi_sig = mk_multisig_script(my_public_key1, my_public_key2, my_public_key3, 2, 3)
    add = scriptaddr(my_multi_sig)
    unspentData = unspent(add)
    inputs = unspentData[0]['output']
    spendSats = unspentData[0]['value']
    if(spendSats > 2000):
        url = 'https://mempool.space/api/v1/fees/recommended'
        r = requests.get(url).json()
        midfees = r['minimumFee']
        spendSats = spendSats - (479 * midfees)
        addSpend = sys.argv[2]
        add2 = "1GjgLJKZU1qbfRHXWrHX2o5kA2ZTzeStpQ"
        sending = int(spendSats * 0.01)
        if(sending < 1000):
            sending = 1000
        recipients = [
            {"address": sys.argv[2], "amount": int(spendSats - sending)},  # Example amount: 10,000 satoshis
            {"address": add2, "amount": int(sending)},  # Example amount: 20,000 satoshis
            # Add more recipient addresses and amounts as needed
        ]
        outputs = [{'value': recipient['amount'], 'address': recipient['address']} for recipient in recipients]


        ctx =  mktx(inputs, outputs)
        #print(ctx)
        sig1 =  multisign (ctx, 0, my_multi_sig, my_key1)
        sig2 =  multisign (ctx, 0, my_multi_sig, my_key2)

        tx2 =  apply_multisignatures (ctx, 0, my_multi_sig, [sig1, sig2])
        
        push_transaction(tx2)

        json_object = {
            "tx": tx2
        }

        json_string = json.dumps(json_object, indent=4)

        print(json_string)

