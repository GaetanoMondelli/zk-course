// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./verifier.sol";

contract Multiplier is Groth16Verifier {
    uint256 public number;
    bool public last_proof;

    event Proved(bool proved);

    function setNumber(uint256 _number) public {
        number = _number;
    }

    function setProof(bool _proof) public {
        last_proof = _proof;
    }

    function checkProof(
        uint256[2] calldata _pA,
        uint256[2][2] calldata _pB,
        uint256[2] calldata _pC,
        uint256[1] calldata _pubSignals
    ) 
        public
     {
        last_proof = verifyProof(_pA, _pB, _pC, _pubSignals);
        emit Proved(last_proof);
    }
}
