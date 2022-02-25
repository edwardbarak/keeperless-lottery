from brownie import accounts, Wei, Lottery
from scripts.deploy import deploy_lottery


# test if contract is owned by deployer
def test_correct_owner():
    lottery = deploy_lottery(3 * 60, Wei("0.01 ether"))
    assert lottery.owner() == accounts[0]


def test_buyTicket():
    # ARRANGE
    lottery = deploy_lottery(3 * 60, Wei("0.01 ether"))
    initialContractBalance = lottery.balance()

    # ACT
    lottery.buyTicket({"from": accounts[1], "value": lottery.ticketPrice()})

    # ASSERT
    # assert that purchaser owns a ticket
    assert lottery.lotteryTickets(lottery.currentLottery(), 0) == accounts[1]

    # assert that contract received eth for the ticket
    assert lottery.balance() == initialContractBalance + lottery.ticketPrice()
