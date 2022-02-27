from brownie import chain, exceptions, accounts, Wei
from fixtures import lottery, _lotteryDuration
import pytest


def test_buyTicket(lottery):
    # ARRANGE
    initialContractBalance = lottery.balance()

    # ACT
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})

    # ASSERT
    # assert that purchaser owns a ticket
    assert lottery.lotteryTickets(lottery.currentLottery(), 0) == accounts[1]

    # assert that contract received the correct amount of eth for the ticket
    assert lottery.balance() == initialContractBalance + lottery.ticketPrice()


def test_buyTicket_incorrectTicketPrice(lottery):
    # test if contract rejects ticket purchase if the incorrect amount of ETH is sent
    # ARRANGE / ACT
    with pytest.raises(Exception) as e:
        lottery.buyTicket(
            {"from": accounts[1], "value": lottery.ticketPrice() - Wei("0.01 ether")}
        )

    # ASSERT
    assert e.typename == "VirtualMachineError"


def test_buyTicket_multipleTickets(lottery):
    # test if multiple tickets can be purchased for a lottery
    # ARRANGE / ACT
    for i in range(1, 4):
        lottery.buyTicket({"from": accounts[i], "value": lottery.ticketPrice()})
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})

    # ASSERT
    for i in range(0, 3):
        assert (
            lottery.lotteryTickets(lottery.currentLottery(), i)
            == accounts[i + 1].address
        )
    assert lottery.lotteryTickets(lottery.currentLottery(), 3) == accounts[1].address
