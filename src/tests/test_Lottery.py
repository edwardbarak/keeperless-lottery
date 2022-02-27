from brownie import chain, exceptions, accounts, Wei
from fixtures import lottery, _lotteryDuration
import pytest

# test if contract is owned by deployer
def test_correct_owner(lottery):
    assert lottery.owner() == accounts[0]
