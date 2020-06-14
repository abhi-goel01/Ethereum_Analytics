"""
Author = Abhishek Goel
Purpose = Read blockchain data and extract whats needed
Reference: https://github.com/validitylabs/EthereumDB
"""

# This function reads block data from Blockchain and formats it for DB load
def read_block_bchain(block, web3):

    # Read data from Blockchain using Web3
    block_bchain_data = web3.eth.getBlock(block)
    block_py_table = dict(block_bchain_data)

    # Change the keys so that there is no clash with other tables
    mapping = {'hash':'blockHash', 'gasUsed':'blockGasUsed',
               'number':'blockNumber','logsBloom':'blockLogsBloom',
               'nonce':'blockNonce'}
    block_py_table = dict((mapping.get(k,k),v) for (k,v) in block_py_table.items())

    # convert data type to be compatible with SQLITE
    hexfields = ['blockHash', 'blockLogsBloom', 'blockNonce', 'extraData', 'mixHash', 'parentHash', 'receiptsRoot', 'sha3Uncles', 'stateRoot', 'transactionsRoot']
    strfields = ['difficulty', 'totalDifficulty', 'uncles']
    for k in block_py_table.keys():
        if k in hexfields:
            block_py_table[k] = web3.toHex(block_py_table[k])
        elif k in strfields:
            block_py_table[k] = str(block_py_table[k])

    # Retrun the formatted data and raw data from Blockchain
    return block_py_table, block_bchain_data



# This function reads transaction data from Blockchain and formats it for DB load
def read_txn_bchain(txn, web3):

    toaddr_type = None
    # Read data from Blockchain using Web3
    txn_bchain_data = web3.eth.getTransaction(txn)
    txn_py_table = dict(txn_bchain_data)

    # Change the keys so that there is no clash with other tables
    mapping = {'hash':'txnHash', 'nonce':'txnNonce', 'value':'txnValue',
               'from':'addrFrom', 'to':'addrTo'}
    txn_py_table = dict((mapping.get(k,k),v) for (k,v) in txn_py_table.items())

    # convert data type to be compatible with SQLITE
    hexfields = ['txnHash']
    strfields = ['txnValue']

    for k in txn_py_table.keys():
        if k in hexfields:
            txn_py_table[k] = web3.toHex(txn_py_table[k])
        elif k in strfields:
            txn_py_table[k] = str(txn_py_table[k])

    # Check and see if the to_address is a contract address or Externally owned address        
    to_addr = txn_py_table['addrTo']
    if to_addr is not None:
        if web3.eth.getCode(to_addr) == b'': toaddr_type = 'EOA'

    # Retrun the formatted data and raw data from Blockchain
    return txn_py_table, txn_bchain_data, toaddr_type


# This function loads the data in SQLITE from the Python table structure
def execute_sql(table_block, table_txn):
    import sqlite3
    import os
    from sql_helper import create_database, update_database

    # Check if the DB already exists in the operating system
    dbname = 'blockchaindb.sqlite'
    db_is_new = not os.path.exists(dbname)

    # Connect to the SQLITE database
    conn = sqlite3.connect(dbname)
    csr = conn.cursor()

    # Create a new database if none exists
    if db_is_new:
        print('creating a new database')
        create_database(csr)
        update_database(csr, table_block, table_txn)
    else:
        update_database(csr, table_block, table_txn)

    # commit the data and close SQL connection
    conn.commit()
    conn.close()


# This functions checks the database to see if a block already exists
def check_if_exists(block):
        import sqlite3
        import os
        from sql_helper import check_database

        flag = None
        # Check if the DB already exists in the operating system
        dbname = 'blockchaindb.sqlite'
        db_is_new = not os.path.exists(dbname)

        if not db_is_new:
            # Connect to the SQLITE database
            conn = sqlite3.connect(dbname)
            csr = conn.cursor()
            flag = check_database(csr, block)
        return flag
        conn.close()
