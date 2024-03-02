// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "ds-test/test.sol";
import {Test, console, Vm} from "forge-std/Test.sol";
import {Multiplier} from "../src/Multiplier.sol";

contract CounterTest is Test {
    Multiplier public multiplier;

    function setUp() public {
        multiplier = new Multiplier();
    }

    function test_last_proof() public {
        vm.recordLogs();
        multiplier.checkProof(
            [
                0x1e59886fd854cb44a6baa3d4990bccde809520d5c5b52789753635528054d59c,
                0x1acfa85a7e30ef6dfb465db4f929a8865c00bfecce0bc7efbd94f5fb0e485cc1
            ],
            [
                [
                    0x047c30ea8cbf859ea119f5fc7c002cd8c4c966bd15b78c61d8db891a1809a211,
                    0x2e215aaf8ab2a015c2a4dc0aa4316ff372888fe66e67816ef78c651ac0425854
                ],
                [
                    0x2c179df89c088df45388a3ca8eb7da0aedb5a5a30c5dc0f5ea7bad9d33932431,
                    0x04d2f426f2eec44fda16bbc50d2624cb8148147e3a3af757c3878934eaad75f1
                ]
            ],
            [
                0x223dcb3168aeb0d4f92bffd621e403b35ac259caa50d2970b7c91605842c0d65,
                0x2d83dea57cea10508722b9e457707dea626f442ec9397fdd8ed94a557cee22f5
            ],
            [
                uint256(
                    0x0000000000000000000000000000000000000000000000000000000000000021
                )
            ]
        );

        Vm.Log[] memory entries = vm.getRecordedLogs();

        console.log("entries.length", entries.length);
        bytes32 proved_event_signature = keccak256("Proved(bool)");

        for (uint256 i; i < entries.length; i++) {
            if (entries[i].topics[0] == proved_event_signature) {
                assertEq(
                    entries[i].topics[0],
                    proved_event_signature,
                    "emitted amount mismatch."
                );
            }

            break;
        }
    }
}
