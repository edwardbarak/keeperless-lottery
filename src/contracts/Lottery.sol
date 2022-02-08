//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Lottery {
    //VARIABLES
    bool internal locked; //Lock to prevent re-entry

    address payable owner;

    //EVENTS

    //MODIFIERS
    modifier isOwner() {
        require(msg.sender == owner);
        _;
    }

    modifier noReentrant() {
        require(!locked, "No re-entrancy");
        locked = true;
        _;
        locked = false;
    }

    //CONSTRUCTOR
    constructor() {
        owner = payable(msg.sender);
        locked = false;
    }

    //FUNCTIONS
    function buyTicket() public payable noReentrant {
        /*
        if lottery is active:
            transfer eth from msg.sender to contract
            create ticket for msg.sender for the current lottery
        else:
            error("lottery is not active")
        */
    }

    function withdrawWinnings() public payable noReentrant {
        /*
        if msg.sender has winnings:
            transfer all eth from contract to msg.sender
        else:
            error("no claimable winnings")
        */
    }

    function withdrawFees() public payable noReentrant isOwner {
        /*
        if fees > 0:
            transfer all fees from contract to msg.sender
        else:
            error("no claimable fees")
        */
    }

    function startNewLottery() public isOwner noReentrant {
        /*
        if block.timestamp >= lotteryEnd:
            selectCurrentLotteryWinner()
            start new lottery 
                currentLottery += 1
                lotteryEnd = block.timestamp + lotteryLifetime
        else:
            error("current lottery has not ended yet")
        */
    }

    function selectCurrentLotteryWinner() internal {
        /*
        _randNum = select random number between 0 and tickets[currentLottery].length
        winner = tickets[currentLottery][_randNum]
        winners[winner] += currentLotteryPot
        currentLotteryPot = 0
        */
    }

    function retireLotteryContract() public isOwner {
        /*
        selectCurrentLotteryWinner()
        withdrawFees()
        only allow winners to withdraw winnings
        */
    }
}
