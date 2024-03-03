'use client'
import { http, createConfig } from 'wagmi'
import { mainnet, sepolia } from 'wagmi/chains'
import { injected, metaMask, safe, walletConnect } from 'wagmi/connectors'
import * as dotenv from 'dotenv';

dotenv.config();
// const projectId = '<WALLETCONNECT_PROJECT_ID>'

export const config = createConfig({
  chains: [mainnet, sepolia],
  connectors: [
    injected(),
    // walletConnect({ projectId }),
    metaMask(),
    safe(),
  ],
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(process.env.RPC_URL),
  },
})
