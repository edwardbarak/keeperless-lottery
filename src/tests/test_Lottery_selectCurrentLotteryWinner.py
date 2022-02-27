from brownie import chain, exceptions, accounts, Wei
from fixtures import lottery, _lotteryDuration
import pytest


def test_buyTicket_selectCurrentLotteryWinner(lottery):
    # test if selectCurrentLotteryWinner() selects a valid winner
    # ARRANGE
    _numberOfTicketPurchasers = 4

    # ACT
    for i in range(_numberOfTicketPurchasers):
        lottery.buyTicket({"from": accounts[i], "value": lottery.ticketPrice()})
    chain.sleep(_lotteryDuration * 2)
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})

    # ASSERT
    _validWinners = [
        account.address for account in accounts[:_numberOfTicketPurchasers]
    ]
    assert any([lottery.winnerEarnings(addr) > 0 for addr in _validWinners])
