from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    # He adds 100 to tx just in case he needs a little more money
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

# Running a test
# To use a keyword search to specify what to test use -k
#     brownie test -k {somekeyword}
#   e.g. brownie test -k test_only_owner_can_withdraw
#
# To be verbose and output print statements during the test use -s
#     brownie test -s
#
# When testing, if no problems are encountered the test is deemed as PASSED
#


def test_only_owner_can_withdraw():
    print("Starting test_only_owner_can_withdraw")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    print("Is local network; running test")
    account = get_account()
    fund_me = deploy_fund_me()
    # REM: The withdraw() function def only allows an owner to call it
    #     REM: function withdraw() public payable onlyOwner....
    # The next line will create an account that is not the owner of the contract.
    #   Calling brownie test -k test_only_owner_can_withdraw with this line
    #   will cause the script to raise an except and consider the test "failed".
    bad_actor = accounts.add()
    # fund_me.withdraw({"from": bad_actor})
    # However, the test SHOULD raise this exception. We want this exception to be
    #   considered a PASS, so nest the fund_me.withdraw() within the  "with
    #   pytest.raises..." statement
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
