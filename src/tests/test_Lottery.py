from brownie import accounts, Lottery
from scripts.deploy import deploy_lottery

# test if contract is owned by deployer
def test_correct_owner():
    lottery = deploy_lottery()
    assert lottery.owner() == accounts[0]
