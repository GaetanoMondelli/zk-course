import { ethers } from 'ethers';
import * as dotenv from 'dotenv';
import * as fs from 'fs';
import * as path from 'path';

dotenv.config();

const main = async () => {
  if (!process.env.RPC_URL || !process.env.PRIVATE_KEY) {
    console.error('Please set RPC_URL and PRIVATE_KEY in your .env file');
    return;
  }

  const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);


  const contractName = 'Multiplier';
  const buildPath = path.join(__dirname, `./out/${contractName}.sol/${contractName}.json`);
  const contractJSON = JSON.parse(fs.readFileSync(buildPath, 'utf8'));
  const contractABI = contractJSON.abi;
  const contractBytecode = contractJSON.bytecode;

  const ContractFactory = new ethers.ContractFactory(
    contractABI,
    contractBytecode,
    wallet
  );

  try {
    console.log('Deploying contract...');
    const contract = await ContractFactory.deploy(/* constructor arguments */);
    const address = await contract.getAddress();
    console.log(`Contract deployed to address: ${address}`);
  } catch (error) {
    console.error('Error in deployment:', error);
  }
};

main().catch((error) => {
  console.error('Unhandled error:', error);
});
