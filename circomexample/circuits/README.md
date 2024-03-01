1. create the circuit
1. Compile it ```circom multiplier2.circom --r1cs --wasm --sym --c```
1. Generate witness: node generate_witness.js multiplier.wasm ../inputs/input.json witness.wtns
1. Powers of Tau
    1. in trusted setup folder ```snarkjs powersoftau new bn128 12 pot12_0000.ptau -v```
    1. circuit specific snarkjs ```powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau -v```
    1. getthe .zkey file ```snarkjs groth16 setup multiplier2.r1cs pot12_final.ptau multiplier2_0000.zkey```
    1. Contribute phase 2 ```snarkjs zkey contribute multiplier2_0000.zkey multiplier2_0001.zkey --name="1st Contributor Name" -v```
1. Export the verification key ```snarkjs zkey export verificationkey multiplier2_0001.zkey verification_key.json```

Now let's generate zk proof associated to the circuit and the witness within this trusted setup
1. ```snarkjs groth16 prove multiplier2_0001.zkey witness.wtns proof.json public.json```

We get:
proof.json: it contains the proof.
public.json: it contains the values of the public inputs and outputs.

Verification

1. To verify the proof, execute the following command:

```snarkjs groth16 verify verification_key.json public.json proof.json```

create a verifier

```snarkjs zkey export solidityverifier multiplier2_0001.zkey verifier.sol```

generate calldata

```snarkjs generatecall``