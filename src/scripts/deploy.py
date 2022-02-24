from tkinter import W
from brownie import Lottery, accounts


def deploy_lottery():
    account = accounts[0]
    lottery = Lottery.deploy({"from": account})
    return lottery


def main():
    deploy_lottery()
