from brownie import FundMe
from scripts.helpful_scripts import get_account
from web3 import Web3


# In order to make this work against ganache-local environment, I needed to
#   change the Ganache UI applications hardfork. See my comments here:
#     https://github.com/smartcontractkit/full-blockchain-solidity-course-py/discussions/422#discussioncomment-1894915

def fund():
    fund_me = FundMe[-1]
    account = get_account()
    print(f"fund(): Account: {account}")
    # Work-around: dividing by 10**8
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account, "gas_limit": 6721975})


def main():
    fund()
    withdraw()
