from brownie import chain, exceptions, accounts, Wei
from fixtures import lottery, _lotteryDuration
import pytest


def test_withdrawFees(lottery):
    # test if owner can withdraw fees
    # ARRANGE
    _initialOwnerBalance = accounts[0].balance()

    # ACT
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})
    lottery.withdrawFees({"from": accounts[0]})

    # ASSERT
    assert accounts[0].balance() > _initialOwnerBalance
    assert lottery.ownerEarnings() == 0
