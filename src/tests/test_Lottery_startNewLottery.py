from brownie import chain, exceptions, accounts, Wei
from fixtures import lottery, _lotteryDuration
import pytest


def test_buyTicket_startNewLottery(lottery):
    # test if buying a new ticket after the first lottery initiates a new lottery
    # ARRANGE / ACT
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})
    chain.sleep(_lotteryDuration * 2)
    lottery.buyTicket({"from": accounts[2], "value": lottery.ticketPrice()})

    # ASSERT
    assert lottery.currentLottery() > 0
    assert lottery.lotteryTickets(0, 0) == accounts[1]
    assert lottery.lotteryTickets(lottery.currentLottery(), 0) == accounts[2]


def test_buyTicket_startNewLottery_noPreviousTickets(lottery):
    # test if a new lottery is properly started if there were no tickets purchased in the previous lottery
    # ARRANGE / ACT
    chain.sleep(_lotteryDuration * 2)
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})
    # ASSERT
    assert lottery.currentLottery() > 0
