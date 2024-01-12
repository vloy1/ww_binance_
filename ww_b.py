from random import randint,uniform
import ccxt
from loguru import logger
import time
from web3 import Web3

file_wal = 'wal.txt'
time_ = 10
EXCHANGE_MIN_AMOUNT_MAIN = 0.009 # минимальный вывод с биржи 
EXCHANGE_MAX_AMOUNT_MAIN = 0.0091 # минимальный вывод с биржи 
MIN_MAIN_WALLET_BALANCE = 0.0054 # минимальный баланс
BINANCE_API_ = {'apiKey':  '',
                'secret' : ''}

w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.defibit.io/'))

def get_balance(address, human=False):
        balance = w3.eth.get_balance(Web3.to_checksum_address(address))
        if not human: return balance
        else: return balance / 10 ** 18

def wait_balance(adress,needed_balance):
        logger.debug(f'[•] Web3 | Waiting for {needed_balance} ETH balance')
        while True:
            try:
                new_balance = get_balance(adress,human=True)
                if new_balance >= needed_balance:
                    logger.debug(f'[•] Web3 | New balance: {round(new_balance, 4)} ETH')
                    break
                time.sleep(5)
            except: pass

def binance_withdraw(address):
        #try:
            SYMBOL = 'BNB'
            NETWORK = 'BEP20'

            old_balance = get_balance(address,human=True)

            if old_balance >= MIN_MAIN_WALLET_BALANCE: return True
            amount_from = EXCHANGE_MIN_AMOUNT_MAIN
            amount_to = EXCHANGE_MAX_AMOUNT_MAIN
            AMOUNT = round(uniform(amount_from, amount_to), 4)


            account_binance = ccxt.binance({
                'apiKey': BINANCE_API_['apiKey'],
                'secret': BINANCE_API_['secret'],
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot'
                }
            })

            account_binance.withdraw(
                code=SYMBOL,
                amount=AMOUNT,
                address=address,
                tag=None,
                params={
                    "network": NETWORK
                }
            )
            logger.success(f"[+] Binance | Success withdraw {AMOUNT} {SYMBOL} to {address}")
            wait_balance(address,needed_balance=old_balance+0.00001)
        #except Exception as error:
                #raise ValueError(f'Binance withdraw error: {error}')
        
def wallett(file):
    try:
        private = open(file,'r').read().splitlines()
        wallet = private[00]
        return wallet
    except:
        logger.error(f'Кошельки кончились {file}')

def wallett_del(file):
    ish = open(file,'r').readlines()
    del ish[00]
    with open(file, "w") as file:
        file.writelines(ish)

def main():
    while True:
        adress = wallett(file_wal)
        try:
            binance_withdraw(adress)
        except:
            logger.info(f'error {adress}')
        wallett_del(file_wal)
        time.sleep(time_)

if __name__ == '__main__':
    main()
