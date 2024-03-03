"use client"
import React, { useEffect, useState } from 'react';
import { ethers } from 'ethers';
import { useReadContract } from 'wagmi'


const Multiplier = ({ contractAddress }: { contractAddress: `0x${string}` }) => {

  const [ABI, setABI] = useState<any>();

  useEffect(() => {
    fetch('/abis/Multiplier.json')
      .then((response) => response.json())
      .then((data) => setABI(data.abi))
      .catch((error) => console.error('Error fetching ABI:', error));
  }, []);

  const { data: number, error, isPending } = useReadContract({
    address: contractAddress,
    abi: ABI,
    functionName: 'number',
  });



  return (
    <div>
      {JSON.stringify(ABI)}
      {contractAddress}
      {
        isPending ? (
          <div>Loading...</div>
        ) : error ? (
          <div>Error: {error.message}</div>
        ) :
          number ?
            (
              <div>Number: {JSON.stringify(
                number

              )}</div>
            )
            : null
      }
    </div>
  );
};

export default Multiplier;
