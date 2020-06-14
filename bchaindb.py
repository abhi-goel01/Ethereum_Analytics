"""
Author: Abhishek Goel
Purpose: Read blockchain data and load into SQLITE database
Reference: https://github.com/validitylabs/EthereumDB
"""

from web3 import Web3
from bchainread import *

# Connect to Blockchain via Infura
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/your-personal-number"))

# add a print statement telling the user about the latest block that exists in the DB
start = input('Enter the starting block number: ')
howmany = input('How many blocks do you want to load: ')
try:
    sblock = int(start)
    nblocks = int(howmany)
except:
    print('Enter a valid number')

# Array of block data that needs to be loaded in DB; this is a table of dictionaries where each item represents one block
table_block = []
table_txn = []

count = 0
count_txn = 0
skipped = 0
EOA_txn_skipped = 0
write_after = 10
# Loop over all the Blocks
for block in range(sblock, sblock+nblocks):

    print('block', block)
    # Check and see if the block already exists in our DB and only load new blocks
    flag = check_if_exists(block)
    if flag == 'Exists':
        skipped = skipped + 1
        continue

    # read Block data from Blockchain, format it and extract what we need
    block_table, block_data = read_block_bchain(block, web3)
    table_block.append(block_table)
    count = count + 1

    # read transactions belonging to the block
    for txn in block_table['transactions']:
        txn_table, txn_data, toaddr_type = read_txn_bchain(txn, web3)
        # Only load those transactions which were sent to a contract
        if toaddr_type == 'EOA':
            EOA_txn_skipped = EOA_txn_skipped + 1
            continue
        table_txn.append(txn_table)
        count_txn = count_txn + 1

    # load the data in SQLITE (every 10 blocks) and print the count
    if (count % write_after) == 0:
        execute_sql(table_block, table_txn)
        del table_block
        del table_txn
        table_block = []
        table_txn = []

print('No. of blocks skipped:',skipped)
print('No. of blocks loaded in DB:',count)
print('No. of EOA transactions skipped:',EOA_txn_skipped)
print('No. of transactions loaded in DB:',count_txn)
