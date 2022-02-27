from brownie import chain, exceptions, accounts, Wei, Lottery
from scripts.deploy import deploy_lottery
import pytest

_lotteryDuration = 3 * 60  # seconds


@pytest.fixture
def lottery():
    return deploy_lottery(_lotteryDuration, Wei("0.01 ether"), Wei("0.0005 ether"))


# test if contract is owned by deployer
def test_correct_owner(lottery):
    assert lottery.owner() == accounts[0]


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
