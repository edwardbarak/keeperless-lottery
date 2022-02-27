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
    constructor(
        uint256 _lotteryDuration,
        uint256 _ticketPrice,
        uint256 _lotteryFee
    ) {
        owner = payable(msg.sender);
        locked = false;
        //start lottery
        lotteryDuration = _lotteryDuration;
        lotteryEnd = block.timestamp + lotteryDuration;
        ticketPrice = _ticketPrice;
        lotteryFee = _lotteryFee;
    }

    //FUNCTIONS
    function buyTicket() external payable noReentrant {
        require(msg.value == ticketPrice);
        if (block.timestamp > lotteryEnd) startNewLottery();
        lotteryTickets[currentLottery].push(msg.sender);
        ownerEarnings += lotteryFee;
        currentLotteryPot += ticketPrice - lotteryFee;
    }

    function withdrawWinnings() external payable noReentrant {
        require(winnerEarnings[msg.sender] > 0);
        payable(msg.sender).transfer(winnerEarnings[msg.sender]);
        winnerEarnings[msg.sender] = 0;
    }

    function withdrawFees() external payable noReentrant isOwner {
        require(ownerEarnings > 0);
        owner.transfer(ownerEarnings);
        ownerEarnings = 0;
    }

    function startNewLottery() private {
        require(block.timestamp > lotteryEnd);
        if (lotteryTickets[currentLottery].length > 0)
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
