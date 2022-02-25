//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Lottery {
    //VARIABLES
    bool internal locked; //Lock to prevent re-entry

    address payable public owner;

    uint256 public lotteryDuration;
    uint256 public lotteryEnd;
    uint256 public currentLottery;
    uint256 public ticketPrice;
    mapping(uint256 => address[]) public lotteryTickets;

    uint256 public lotteryFee;

    mapping(address => uint256) public winnerEarnings;
    uint256 public ownerEarnings;

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
    constructor(uint256 _lotteryDuration, uint256 _ticketPrice) {
        owner = payable(msg.sender);
        locked = false;
        //start lottery
        lotteryDuration = _lotteryDuration;
        lotteryEnd = block.timestamp + lotteryDuration;
        ticketPrice = _ticketPrice;
    }

    //FUNCTIONS
    function buyTicket() external payable noReentrant {
        require(block.timestamp < lotteryEnd);
        require(msg.value == ticketPrice);
        lotteryTickets[currentLottery].push(msg.sender);
    }

    function withdrawWinnings() external payable noReentrant {
        /*
        if msg.sender has winnings:
            transfer all eth from contract to msg.sender
        else:
            error("no claimable winnings")
        */
    }

    function withdrawFees() external payable noReentrant isOwner {
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
