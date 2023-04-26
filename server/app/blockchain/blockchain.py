from web3 import Web3, HTTPProvider
import json
import os
import solcx

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Blockchain():
    def __init__(self):
        self.contract_file = "contract.sol"
        self.compiled_contract_file = "compiled_contract.json"
        self.contract_name = "SupplyChain"
        self.private_key = "0x4073cbbd66d71ca7b64099132e0f822d3952426369fed7bc71ab7d5b19487337"
        self.chain_id = 1337

        self.web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        self.address = self.web3.eth.defaultAccount
    
    # compile contract and save compiled contract json file
    def compile_contract(self):
        with open(os.path.join(BASEDIR, self.contract_file), 'r') as f:
            source_sol_file = f.read()
        compiled_sol = solcx.compile_standard(
            {
                "language": "Solidity",
                "sources": {self.contract_file: {"content": source_sol_file}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version="0.8.17",
        )
        with open(os.path.join(BASEDIR, self.compiled_contract_file), 'w') as f:
            f.write(json.dumps(compiled_sol))
        
        self.abi = compiled_sol["contracts"][self.contract_file][self.contract_name]["abi"]
        self.bytecode = compiled_sol["contracts"][self.contract_file][self.contract_name]["evm"]["bytecode"]["object"]
        
    # get contract
    def get_constact(self):
        self.compile_contract()
        
        Contract = self.web3.eth.contract(
            abi=self.abi, bytecode=self.bytecode
        )
        nonce = self.web3.eth.getTransactionCount(self.address)
        transaction = Contract.constructor().buildTransaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.web3.eth.gas_price,
                "from": self.address,
                "nonce": nonce,
            }
        )
        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        self.contract_address = tx_receipt.contractAddress
        self.contract = Contract(address=tx_receipt.contractAddress)
        return self.contract
    
    def test_connection(self):
        return self.contract.functions["connectTest"]().call()        
      
    # cost no gas
    def read_contract(self, func, **kwargs):
        return self.contract.functions[func](**kwargs).call()
    
    # cost gas
    def interact_contract(self, func, **kwargs):
        tx = self.contract.functions[func](**kwargs).buildTransaction(
            {
                "from": self.address,
                "gas": 1000000,
                "gasPrice": self.web3.eth.gas_price,
                "nonce": self.web3.eth.getTransactionCount(self.address),
            }
        )
        tx_create = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
        if tx_receipt.status == 1:
            return True
        return False


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.get_constact()
    # print(blockchain.test_connection())
    print(blockchain.interact_contract('addProduct', productName=Web3.toBytes(text='test'), productDescription=Web3.toBytes(text='test')))