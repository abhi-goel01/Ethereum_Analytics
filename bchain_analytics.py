"""
Author: Abhishek Goel
Purpose: Read blockchain data loaded into SQLITE database and create visualization
"""

from web3 import Web3
import sqlite3
import urllib.request, urllib.parse, urllib.error
import ssl
import json

# Connect to Blockchain via Infura
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/your-personal-number"))

# Connect to the SQLITE database
dbname = 'blockchaindb.sqlite'
conn = sqlite3.connect(dbname)
csr = conn.cursor()

# Analysis no. 1 - Find out the top 5 contracts that were called in the last n blocks
csr.execute("SELECT addrto, count(*) FROM txns GROUP BY addrTo ORDER BY 2 DESC LIMIT 5")
try:
    data = csr.fetchall()
except:
    quit()
conn.close()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Write the header data in a JS file which will be used for visualization
fhand = open('bchain_top5_contracts.js','w')
fhand.write("gline = [ ['Contract Name','Count']")

#Fetch contract name for top 5 contracts
for item in data:
    # Prepare the URL to be called for fetching the contract name
    serviceurl = 'https://api.etherscan.io/api?module=contract&action=getsourcecode&'
    api_key = 'your-api-key'
    parms = dict()
    parms["address"] = item[0]
    parms["apikey"] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    #print('calling URL',url)
    uh = urllib.request.urlopen(url, context=ctx)
    etherscan_data = uh.read().decode()

    # Load the JSON response from the API
    try: js = json.loads(str(etherscan_data))
    except: continue

    # Read the contract name
    if not('status' in js and js['status'] == '1') : continue
    contract_name = js["result"][0]["ContractName"]
    #print('contract name',contract_name,' , ','count',item[1])

    # Write the body of the JS file
    fhand.write(",\n['"+contract_name+"',"+str(item[1])+"]")
fhand.write("\n];\n")
fhand.close()

print("Output written to bchain_top5_contracts.js")
print("Open bchain_top5_contracts.htm to visualize the data")
