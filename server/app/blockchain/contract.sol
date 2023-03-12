pragma solidity ^0.8.0;
// SPDX-License-Identifier: MIT


contract SupplyChain {
    enum ParticipantType {supplier, manufactor, distributor, retailer, customer}
    enum ShipmentStatus {inbound, outbound}

    uint constant MAX_STRING_LENGTH = 32;

    struct Product {
        bytes32 productName;
        bytes32 productDescription;
        bytes32[] productShipments;
    }

    struct Participant {
        bytes32 participantName;
        bytes32 participantDescription;
        ParticipantType participantType; // shipment ID
    }

    struct Shipment {
        uint shipmentStartTime;
        uint shipmentEndTime;
        bytes32 participant; // participants ID
        bytes32 shipmentFrom; // Participant ID
        bytes32 shipmentTo; // Participant ID
        ShipmentStatus shipmentStatus; // inbound or outbound
    }

    mapping(bytes32 => Product) products;
    mapping(bytes32 => Shipment) shipments;
    mapping(bytes32 => Participant) participants;

    uint private nextProductNonce = 0;
    uint private nextShipmentNonce = 0;
    uint private nextParticipantNonce = 0;

    event ProductAdded(
        address _sender, 
        bytes32 _productId, 
        bytes32 _productName, 
        bytes32 _productDescription
    );

    function getNextProductId() private returns (bytes32) {
        nextProductNonce += 1;
        return keccak256(abi.encodePacked(nextProductNonce, "PRODUCT_ID"));
    }

    function getNextShipmentId() private returns (bytes32) {
        nextShipmentNonce += 1;
        return keccak256(abi.encodePacked(nextShipmentNonce, "SHIPMENT_ID"));
    }

    function getNextParticipantId() private returns (bytes32) {
        nextParticipantNonce += 1;
        return keccak256(abi.encodePacked(nextParticipantNonce, "PARTICIPANT_ID"));
    }

    // PRODUCT
    function addProduct(bytes32 productName, bytes32 productDescription) public {
        require(productName.length <= MAX_STRING_LENGTH, "Product name is too long");
        require(productDescription.length <= MAX_STRING_LENGTH, "Product description is too long");
        bytes32 productId = getNextProductId();
        products[productId] = Product(productName, productDescription, new bytes32[](0));
        emit ProductAdded(msg.sender, productId, productName, productDescription);
    }

    function updateProduct(bytes32 productId, 
                           bytes32 productName, 
                           bytes32 productDescription) public returns (bool, bytes32){
        if(productName.length <= MAX_STRING_LENGTH) {
            return (false, stringToBytes32("Product name is too long"));
        }
        if(productDescription.length <= MAX_STRING_LENGTH) {
            return (false, stringToBytes32("Product description is too long"));
        }
        products[productId].productName = productName;
        products[productId].productDescription = productDescription;
        return (true, stringToBytes32("success"));
    }

    function getProduct(bytes32 productId) public view returns (bytes32, bytes32, bytes32[] memory) {
        return (products[productId].productName, products[productId].productDescription, products[productId].productShipments);
    }

    // SHIPMENT
    function startShipment(bytes32 prodcutId,
                           bytes32 participant,
                           bytes32 shipmentFrom,
                           bytes32 shipmentTo) public returns (bool, bytes32){
        if (products[prodcutId].productShipments.length > 0) {
            uint lastShipmentIndex = products[prodcutId].productShipments.length-1;
            bytes32 lastShipmentId = products[prodcutId].productShipments[lastShipmentIndex];
            if (shipments[lastShipmentId].shipmentStatus != ShipmentStatus.outbound) {
                return (false, stringToBytes32("Shipment didn't end yet"));
            }
            if (shipments[lastShipmentId].shipmentTo != shipmentFrom) {
                return (false, stringToBytes32("Shipment from doesn't match last shipment to"));
            }
        }
        bytes32 shipmentId = getNextShipmentId();
        shipments[shipmentId] = Shipment(block.timestamp, 0, participant, shipmentFrom, shipmentTo, ShipmentStatus.inbound);
        products[prodcutId].productShipments.push(shipmentId);
        return (true, shipmentId);
    }

    function endShipment(bytes32 shipmentId) public {
        // uint lastShipmentIndex = products[prodcutId].productShipments.length-1;
        // bytes32 lastShipmentId = products[prodcutId].productShipments[lastShipmentIndex];
        shipments[shipmentId].shipmentEndTime = block.timestamp;
        shipments[shipmentId].shipmentStatus = ShipmentStatus.outbound;
    }

    function getShipments(bytes32[] memory shipmentIds) public view returns (Shipment[] memory){
        Shipment[] memory result = new Shipment[](shipmentIds.length);
        for (uint i = 0; i < shipmentIds.length; i++) {
            result[i] = shipments[shipmentIds[i]];
        }
        return result;
    }

    // PARTICIPANT
    function createParticipant(bytes32 participantName, bytes32 participantDescription, ParticipantType participantType) public returns(bool, bytes32) {
        if (participantName.length > MAX_STRING_LENGTH) {
            return (false, stringToBytes32("Participant name is too long"));
        }
        if (participantDescription.length > MAX_STRING_LENGTH) {
            return (false, stringToBytes32("Participant description is too long"));
        }
        bytes32 participantId = getNextParticipantId();
        participants[participantId] = Participant(participantName, participantDescription, participantType);
        return (true, "success");
    }

    function updateParticipant(bytes32 participantId, bytes32 participantName, bytes32 participantDescription, ParticipantType participantType) public returns(bool, bytes32) {
        if (participantName.length > MAX_STRING_LENGTH) {
            return (false, stringToBytes32("Participant name is too long"));
        }
        if (participantDescription.length > MAX_STRING_LENGTH) {
            return (false, stringToBytes32("Participant description is too long"));
        }
        participants[participantId].participantName = participantName;
        participants[participantId].participantDescription = participantDescription;
        participants[participantId].participantType = participantType;
        return (true, "success");
    }

    // UTILS
    function stringToBytes32(string memory source) private pure returns(bytes32 result){
        assembly{
            result := mload(add(source,32))
        }
        return result;
    }

    function connectTest() public pure returns(bool) {
        return true;
    }

    function testAddProduct(bytes32 productName, bytes32 productDescription) public returns (bytes32) {
        bytes32 productId = getNextProductId();
        products[productId] = Product(productName, productDescription, new bytes32[](0));
        return productId;
    }
}