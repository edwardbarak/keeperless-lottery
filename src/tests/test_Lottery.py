from brownie import exceptions, accounts, Wei, Lottery
from scripts.deploy import deploy_lottery
import pytest

_lotteryDuration = 3 * 60  # seconds


@pytest.fixture
def lottery():
    return deploy_lottery(_lotteryDuration, Wei("0.01 ether"))


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
    # ACT
    with pytest.raises(Exception) as e:
        lottery.buyTicket(
            {"from": accounts[1], "value": lottery.ticketPrice() - Wei("0.01 ether")}
        )

    # ASSERT
    assert e.typename == "VirtualMachineError"


# def test_buyTicket_startNewLottery(lottery):
# test if buying a new ticket after the first lottery initiates a new lottery
# ARRANGE
# ACT
# ASSERT

# def test_buyTicket_selectCurrentLotteryWinner(lottery):
# test if selectCurrentLotteryWinner() selects a valid winner
# ARRANGE
# ACT
# ASSERT
