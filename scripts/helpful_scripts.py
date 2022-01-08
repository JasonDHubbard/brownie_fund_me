from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
# Starting price = 2000 * 10**8
# Want it to be same as FundMe's getPrice() function
STARTING_PRICE = 200000000000
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    print("Starting helpful_scripts.py: get_account()...")
    active_network = network.show_active()
    print(f"  Network: {active_network}")
    if active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS or active_network in FORKED_LOCAL_ENVIRONMENTS:
        account = accounts[0]
        print("    Local network")
        print(f"    Returning account 0: {account}")
    else:
        configured_wallet = config["wallets"]["from_key"]
        print("    Non-local network")
        print(f"    Returning configured account: {configured_wallet}")
        account = accounts.add(configured_wallet)
    print("...Ending helpful_scripts.py: get_account() with return")
    return account


def deploy_mocks():
    print("Starting helpful_scripts.py: deploy_mocks()...")
    active_network = network.show_active()
    if len(MockV3Aggregator) <= 0:
        print("  MockV3Aggregator not yet deployed")
        print("  Calling MockV3Aggregator.sol: deploy()")
        # See MockV3Aggregators constructor...
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("  Mocks deployed")
    else:
        print("  MockV3Aggregator already deployed")
    print("...Ending helpful_scripts.py: deploy_mocks()")
