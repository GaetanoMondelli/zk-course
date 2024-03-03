'use client';
import Image from "next/image";
import styles from "./page.module.css";
import { WagmiProvider, useAccount } from 'wagmi';
import { config } from '../../config';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Multiplier from './Multiplier';
import { Account } from './accounts' 
import { WalletOptions } from './walletOptions' 

function ConnectWallet() { 
  const { isConnected } = useAccount() 
  if (isConnected) return <Account /> 
  return <WalletOptions /> 
} 



const queryClient = new QueryClient();

export default function Home() {
  const contractAddress = "0x8c0Cd795a947b256C8e99fe9b6D82F1C3eCbd82e";

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <ConnectWallet /> 
        <p>Provider</p>
        <Multiplier contractAddress={contractAddress} />
      </QueryClientProvider>
    </WagmiProvider>
  );
}
