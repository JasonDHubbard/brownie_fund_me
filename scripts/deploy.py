from brownie import FundMe, MockV3Aggregator, network, config

# May need to create an __init__.py in the scripts directory for this import to work.
#   It depends on the version of Python being used
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS
)

# To add our ganache development network to our list of remembered Etherium networks:
#     brownie networks add Ethereum ganache-local host=http://127.0.0.1:8545 chainid=1337
#   ... where "ganache-local" is the name we're giving it
#   ... and host is either the UI or cli ganache network address
#
# Timestamp 6:01:00...
# To create a development mainnet fork via infura, you run the following...
#     brownie networks add development mainnet-fork-dev cmd=ganache-cli
#       host=http://127.0.0.1 port=8545
#       fork='https://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID'
#       accounts=10 mnemonic=brownie
#  ... where the fork is in single-quotes so that the environment variable is
#    is swapped properly.
#  He said, however, that these mainnet-forks haven't worked well for him in infura.
#
# To create a development mainnet fork via Alchemy.com, sign up with Alchemy.com and
#   follow steps to create new app with:
#     Environment: Development
#     Chain: Ethereum
#     Network: Mainnet
# Run the following at the command line to add the network...
#     brownie networks add development mainnet-fork-dev cmd=ganache-cli
#       host=http://127.0.0.1 fork='https://eth-mainnet.alchemyapi.io/v2/AwAzQC5uqisUWddss_CKIgWzez61a-U8'
#       accounts=10 mnemonic=brownie port=8545
# ...where the fork is the http url found under the "VIEW KEY" button for the application
#   in Alchemy


def deploy_fund_me():
    print("Starting deploy.py: deploy_fund_me()...")
    account = get_account()

    # If we're on a persistent network like rinkeby, use the associated
    #   address, otherwise deploy mocks
    #
    active_network = network.show_active()
    if active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][active_network]["eth_usd_price_feed"]
        print(
            f"  Using configured {active_network} pricefeed address: {price_feed_address}")
    else:
        # For local environments
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        print(
            f"  Using MockV3Aggregator pricefeed address: {price_feed_address}")

    # Adding publish_source=True will submit our source for verification. It will
    #   need the ETHERSCAN_TOKEN value from the .env file.
    # ".get("verify") is being used instead of ["verify"] as it is more forgiving
    #   if you forgot to add the "verify:" value in the config yaml
    print("  Calling fundme.sol: FundMe.deploy()")
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"  FundMe contract deployed to {fund_me.address}")
    print("...Ending deploy.py: deploy_fund_me()")
    return fund_me


def main():
    deploy_fund_me()
