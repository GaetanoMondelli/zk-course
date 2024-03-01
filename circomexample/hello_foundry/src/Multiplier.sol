// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./verifier.sol";

contract Multiplier is Groth16Verifier {
    uint256 public number;
    event Proved(bool proved);

    function checkProof(
        uint256[2] calldata _pA,
        uint256[2][2] calldata _pB,
        uint256[2] calldata _pC,
        uint256[1] calldata _pubSignals
    ) public
     {
        emit Proved(verifyProof(_pA, _pB, _pC, _pubSignals));
    }
}
