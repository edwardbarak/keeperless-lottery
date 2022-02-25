from tkinter import W
from brownie import Lottery, accounts


def deploy_lottery(_lotteryDuration, _ticketPrice):
    account = accounts[0]
    lottery = Lottery.deploy(_lotteryDuration, _ticketPrice, {"from": account})
    return lottery


def main():
    deploy_lottery()
