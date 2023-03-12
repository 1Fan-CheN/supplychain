import yaml
import os
import logging.config
from flask import Flask
from config import Config
from web3 import Web3

BASEDIR = os.path.abspath(os.path.dirname('..'))
env = os.environ.get('FLASK_ENV', 'development')

def create_log(env):
    with open(BASEDIR + '/LogConfig.yaml', 'r') as f:
        try:
            log_config = yaml.load(f.read(), Loader=yaml.FullLoader)
        except:
            log_config = yaml.safe_load(f.read())
        log_config['handlers']['info_file_handler']['filename'] = os.path.join(BASEDIR, 'info.log')
        log_config['handlers']['error_file_handler']['filename'] = os.path.join(BASEDIR, 'error.log')
        logging.config.dictConfig(log_config)
        if env == 'production':
            return logging.getLogger(__name__)
        else:
            return logging.getLogger('DEBUG')
        
def create_app(env):
    app = Flask(__name__)
    app.config.from_object(Config[env])
    from app.routes.user import users as users_blueprint
    app.register_blueprint(users_blueprint)
    
    return app

def create_blockchain():
    from app.blockchain.blockchain import Blockchain
    blockchain = Blockchain()
    
    return blockchain

def create_contract(blockchain):
    contract = blockchain.get_constact()
    logger.info('============================================================')
    logger.info('Address: ' + str(blockchain.address))
    logger.info('Private Key: ' + blockchain.private_key)
    logger.info('Balance(Ether): '+ str(Web3.fromWei(blockchain.web3.eth.getBalance(blockchain.address), 'ether')))
    logger.info("Contract deployed to: " + str(blockchain.contract_address))
    logger.info('============================================================')
    return contract

app = create_app(env)
logger = create_log(env)
blockchain = create_blockchain()
contract = create_contract(blockchain)

__all__ = ['app', 'logger', 'blockchain', 'contract']
