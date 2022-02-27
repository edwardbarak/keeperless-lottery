from brownie import accounts, Wei, Lottery
from scripts.deploy import deploy_lottery
import pytest

_lotteryDuration = 3 * 60


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

    # assert that contract received eth for the ticket
    assert lottery.balance() == initialContractBalance + lottery.ticketPrice()
