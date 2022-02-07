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
    function buyTicket() public payable noReentrant {}

    function withdrawWinnings() public payable noReentrant {}

    function withdrawFees() public payable noReentrant isOwner {}

    function startLottery() public isOwner {}

    function endLottery() public isOwner {}
}
