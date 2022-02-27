//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Lottery {
    //VARIABLES
    bool private locked; //Lock to prevent re-entry

    address payable public owner;

    uint256 public lotteryDuration;
    uint256 public lotteryEnd;
    uint256 public currentLottery;
    uint256 public currentLotteryPot;
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
        require(msg.value == ticketPrice);
        if (block.timestamp > lotteryEnd) startNewLottery();
        lotteryTickets[currentLottery].push(msg.sender);
        //TODO: pay fee to contract owner
        //TODO: increment lottery pot
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

    function startNewLottery() private {
        require(block.timestamp > lotteryEnd);
        selectCurrentLotteryWinner();
        currentLottery += 1;
        lotteryEnd = block.timestamp + lotteryDuration;
    }

    function selectCurrentLotteryWinner() private {
        uint256 _randNum = uint256(
            keccak256(abi.encodePacked(block.difficulty, block.timestamp))
        ); //TODO: replace with chainlink VRF

        uint256 _winningTicket = _randNum %
            lotteryTickets[currentLottery].length;

        address _winningAddress = lotteryTickets[currentLottery][
            _winningTicket
        ];

        winnerEarnings[_winningAddress] += currentLotteryPot;
        currentLotteryPot = 0;
    }

    function retireLotteryContract() public isOwner {
        /*
        selectCurrentLotteryWinner()
        withdrawFees()
        only allow winners to withdraw winnings
        */
    }
}
