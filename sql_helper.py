"""
Author = Abhishek Goel
Purpose = Execute SQL commands to interact with SQLITE database
Reference = https://github.com/validitylabs/EthereumDB
"""

# This function creates a new database
def create_database(csr):

    blck = """
    CREATE TABLE IF NOT EXISTS blocks(
     blockNumber INTEGER PRIMARY KEY,
     blockHash TEXT,
     miner TEXT,
     blockNonce TEXT,
     blockGasUsed INTEGER,
     gasLimit INTEGER,
     timestamp INTEGER);
    """
    csr.execute(blck)

    txn = """
    CREATE TABLE IF NOT EXISTS txns(
     txnHash TEXT PRIMARY KEY,
     blockNumber INTEGER,
     txnNonce INTEGER,
     txnValue TEXT,
     addrFrom TEXT,
     addrTo TEXT);
    """
    csr.execute(txn)

# This function updates the tables in database
def update_database(csr, table_block, table_txn):
    blck = """ INSERT INTO blocks VALUES (:blockNumber, :blockHash, :miner, :blockNonce, :blockGasUsed, :gasLimit, :timestamp) """
    csr.executemany(blck, table_block)

    txn = """ INSERT INTO txns VALUES (:txnHash, :blockNumber, :txnNonce, :txnValue, :addrFrom, :addrTo) """
    csr.executemany(txn, table_txn)

# This function checks the database to see if a block already exists
def check_database(csr, block):
    csr.execute("SELECT blockNumber FROM blocks WHERE blockNumber = ?",(block,))
    try:
        data = csr.fetchone()[0]
        print('Skipping Block',block,'as it already exists in the DB')
        flag = 'Exists'
    except:
        flag = 'does not exist'
    return flag
