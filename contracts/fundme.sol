// SPDX-License-Identifier: MIT

// To create a new project in a folder run
//   brownie init
// To compile the contract use the command
//   brownie compile
// After compiling this file, you should see under build/contracts:
//   A dependencies folder with the imported sol files
//   FundMe.json

pragma solidity >=0.6.6 <=0.9.0;

// These imports which worked in Remix will not work in Brownie automatically.
//   Remix can download packages directly from npm. Brownie can download directly
//   from Github. Need to create a "remmapping" of "@chainlink" in brownie-config.yaml.
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    // sets the owner to whomever deploys this contract
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        // Set minimum amount of USD in ETH to send to $50
        uint256 minimumUSD = 50 * 10**18;
        // Will revert the transaction (send money back + unspent gas) if requirement
        //   not met.
        // Commented out require as work-around
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "Minimum of $50 USD in ETH required!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        // Also adding to this array for the purpose of this training
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        return uint256(answer * 10000000000); // e.g. returns 3940310000000000000000
    }

    //If buying 1 GWEI which is 1000000000 WEI
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 1000000000000000000; // e.g. returns 3897810000000
        return ethAmountInUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    // function modifier
    modifier onlyOwner() {
        // Will only allow the function it modifies to run if the
        //   address making the call (i.e. the sender) is this contract's
        //   address.
        require(msg.sender == owner);
        _; // now run the function here
    }

    function withdraw() public payable onlyOwner {
        // "this" means this contract (at the contract's address)
        msg.sender.transfer(address(this).balance);
        // loop through the array and set everybody's balance to zero
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            // grab funder address
            address funder = funders[funderIndex];
            // set funder amount to 0
            addressToAmountFunded[funder] = 0;
        }
        // "reset" the array
        funders = new address[](0);
    }
}
