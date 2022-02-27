from tkinter import W
from brownie import Lottery, accounts


def deploy_lottery(_lotteryDuration, _ticketPrice, _lotteryFee):
    account = accounts[0]
    lottery = Lottery.deploy(
        _lotteryDuration, _ticketPrice, _lotteryFee, {"from": account}
    )
    return lottery


def main():
    deploy_lottery()
