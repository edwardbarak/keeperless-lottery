from brownie import Wei, Lottery
from scripts.deploy import deploy_lottery
import pytest

_lotteryDuration = 3 * 60  # seconds


@pytest.fixture
def lottery():
    return deploy_lottery(_lotteryDuration, Wei("0.01 ether"), Wei("0.0005 ether"))
