# Ethereum_Analytics (Python and SQLITE)

Perform analytics on the data residing in Ethereum blockchain. Database management system used is: SQLite

## Environment setup
1. Install web3 using pip
    - If you have Python3 installed then pip comes along with it
    - Simply type the following command in the terminal window:
      $ pip3 install web3

2. Create an account on [Infura](https://www.infura.io) so that you can connect with Ethereum main net using their nodes or run a local node
    - Create a project in Infura
    - After this you will get your end point through which you can connect to the node
    - use the following to connect with blockchain as per your preference

    ```python
    # 1. connection via Infura
    #web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/your-personal-number"))

    # 2. or connection via local node
    #web3 = Web3(Web3.IPCProvider('/your-path-to/geth.ipc'))
    ```

3. We are also going to use Etherscan API so:
    - Create an account on [Etherscan](https://www.etherscan.io)
    - Generate your own API KEY

4. Download DB browser for SQLITE which we can use for querying the data that we load in SQLITE database

## Python programs
1. bchaindb.py, bchainread.py, sql_helper.py
    - using these programs we will read blockchain data and load into SQLITE database
    - warning: do not load data for too many blocks at one go as it may cause the program to run for long time

2. bchain_analytics.py
    - Using this program we will do our first analysis which is to find the top 5 contracts that were called by the transactions
    - This program also loads the results into a JS file which will then be used for visualization
    - open the bchain_top5_contracts.htm to see the result
