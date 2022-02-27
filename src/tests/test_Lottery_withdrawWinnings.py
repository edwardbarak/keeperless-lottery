from brownie import chain, exceptions, accounts, Wei
from fixtures import lottery, _lotteryDuration
import pytest


def test_withdrawFees(lottery):
    # test if owner can withdraw fees
    # ARRANGE / ACT
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})
    chain.sleep(_lotteryDuration * 2)
    lottery.buyTicket({"from": accounts[2], "value": lottery.ticketPrice()})
    _account1Winnings = lottery.winnerEarnings(accounts[1].address)
    _account1PostWinBalance = accounts[1].balance()
    lottery.withdrawWinnings({"from": accounts[1]})

    # ASSERT
    # assert accounts[0].balance() > _initialOwnerBalance
    # assert lottery.ownerEarnings() == 0
    assert _account1Winnings > 0
    assert accounts[1].balance() == _account1PostWinBalance + _account1Winnings
    assert lottery.winnerEarnings(accounts[1].address) == 0
