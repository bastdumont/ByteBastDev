/**
 * Cryptocurrency Transaction Service
 * Handles sending crypto to user wallets after payment confirmation
 */

import { ethers } from 'ethers';
import * as bitcoin from 'bitcoinjs-lib';

export interface CryptoTransaction {
  txHash: string;
  status: 'pending' | 'confirmed' | 'failed';
  confirmations: number;
  networkFee: string;
  timestamp: Date;
}

export interface SendCryptoParams {
  cryptoCurrency: string;
  amount: string;
  toAddress: string;
  transactionId: string;
}

/**
 * Send cryptocurrency to user's wallet
 */
export async function sendCrypto(params: SendCryptoParams): Promise<CryptoTransaction> {
  const { cryptoCurrency, amount, toAddress, transactionId } = params;

  console.log(`Sending ${amount} ${cryptoCurrency} to ${toAddress}`);

  try {
    switch (cryptoCurrency) {
      case 'ETH':
      case 'USDC':
      case 'USDT':
        return await sendEthereumTransaction(cryptoCurrency, amount, toAddress, transactionId);

      case 'BTC':
        return await sendBitcoinTransaction(amount, toAddress, transactionId);

      default:
        throw new Error(`Unsupported cryptocurrency: ${cryptoCurrency}`);
    }

  } catch (error: any) {
    console.error('Error sending crypto:', error);

    // Update transaction status to failed
    await updateTransactionStatus(transactionId, 'failed', error.message);

    throw error;
  }
}

/**
 * Send Ethereum or ERC-20 token
 */
async function sendEthereumTransaction(
  currency: string,
  amount: string,
  toAddress: string,
  transactionId: string
): Promise<CryptoTransaction> {
  // Initialize provider
  const provider = new ethers.JsonRpcProvider(
    process.env.ETHEREUM_RPC_URL || 'https://eth-mainnet.g.alchemy.com/v2/demo'
  );

  // Initialize wallet
  const wallet = new ethers.Wallet(
    process.env.ETHEREUM_HOT_WALLET_PRIVATE_KEY!,
    provider
  );

  let tx: ethers.TransactionResponse;

  if (currency === 'ETH') {
    // Send native ETH
    tx = await wallet.sendTransaction({
      to: toAddress,
      value: ethers.parseEther(amount),
      gasLimit: 21000
    });

  } else {
    // Send ERC-20 token (USDC or USDT)
    const tokenAddress = getTokenAddress(currency);
    const tokenContract = new ethers.Contract(
      tokenAddress,
      ['function transfer(address to, uint amount) returns (bool)'],
      wallet
    );

    // Convert amount based on token decimals (USDC and USDT use 6 decimals)
    const decimals = currency === 'USDC' || currency === 'USDT' ? 6 : 18;
    const tokenAmount = ethers.parseUnits(amount, decimals);

    tx = await tokenContract.transfer(toAddress, tokenAmount);
  }

  // Wait for transaction receipt
  const receipt = await tx.wait();

  if (!receipt) {
    throw new Error('Transaction receipt not available');
  }

  // Calculate network fee
  const networkFee = ethers.formatEther(
    receipt.gasUsed * receipt.gasPrice
  );

  // Update transaction in database
  await updateTransactionStatus(transactionId, 'crypto_sent', undefined, tx.hash);

  return {
    txHash: tx.hash,
    status: 'pending',
    confirmations: receipt.confirmations,
    networkFee,
    timestamp: new Date()
  };
}

/**
 * Send Bitcoin transaction
 */
async function sendBitcoinTransaction(
  amount: string,
  toAddress: string,
  transactionId: string
): Promise<CryptoTransaction> {
  // This is a simplified example - production should use a proper Bitcoin library/service
  // Consider using services like BitGo, Coinbase Commerce, or running your own Bitcoin node

  const satoshis = Math.floor(parseFloat(amount) * 100000000); // Convert BTC to satoshis

  // Placeholder for actual Bitcoin transaction
  // In production, you would:
  // 1. Fetch UTXOs for the hot wallet
  // 2. Create transaction inputs and outputs
  // 3. Sign transaction with private key
  // 4. Broadcast to Bitcoin network

  const mockTxHash = '0x' + Array(64).fill(0).map(() =>
    Math.floor(Math.random() * 16).toString(16)
  ).join('');

  await updateTransactionStatus(transactionId, 'crypto_sent', undefined, mockTxHash);

  return {
    txHash: mockTxHash,
    status: 'pending',
    confirmations: 0,
    networkFee: '0.0001', // Typical Bitcoin fee
    timestamp: new Date()
  };
}

/**
 * Get ERC-20 token contract address
 */
function getTokenAddress(currency: string): string {
  // Mainnet addresses
  const addresses: Record<string, string> = {
    'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7'
  };

  // For testnet, use different addresses
  if (process.env.USE_TESTNET === 'true') {
    return addresses[currency + '_TESTNET'] || addresses[currency];
  }

  return addresses[currency];
}

/**
 * Monitor transaction confirmations
 */
export async function monitorTransaction(
  txHash: string,
  cryptoCurrency: string,
  requiredConfirmations: number = 12
): Promise<void> {
  if (cryptoCurrency === 'BTC') {
    await monitorBitcoinTransaction(txHash, requiredConfirmations);
  } else {
    await monitorEthereumTransaction(txHash, requiredConfirmations);
  }
}

/**
 * Monitor Ethereum transaction
 */
async function monitorEthereumTransaction(
  txHash: string,
  requiredConfirmations: number
): Promise<void> {
  const provider = new ethers.JsonRpcProvider(process.env.ETHEREUM_RPC_URL!);

  const checkConfirmations = async () => {
    const receipt = await provider.getTransactionReceipt(txHash);

    if (!receipt) {
      // Transaction not yet mined
      setTimeout(checkConfirmations, 15000); // Check every 15 seconds
      return;
    }

    const currentBlock = await provider.getBlockNumber();
    const confirmations = currentBlock - receipt.blockNumber + 1;

    console.log(`Transaction ${txHash} has ${confirmations} confirmations`);

    if (confirmations >= requiredConfirmations) {
      // Transaction confirmed
      await finalizeTransaction(txHash);
    } else {
      // Keep monitoring
      setTimeout(checkConfirmations, 15000);
    }
  };

  await checkConfirmations();
}

/**
 * Monitor Bitcoin transaction
 */
async function monitorBitcoinTransaction(
  txHash: string,
  requiredConfirmations: number
): Promise<void> {
  // Placeholder - implement Bitcoin transaction monitoring
  // Use blockchain.info API, blockchair.com, or your own Bitcoin node

  console.log(`Monitoring Bitcoin transaction: ${txHash}`);

  // For production, implement actual monitoring
  setTimeout(async () => {
    await finalizeTransaction(txHash);
  }, 60000); // Simulate 1 minute delay
}

/**
 * Validate cryptocurrency address
 */
export function validateAddress(address: string, currency: string): boolean {
  try {
    if (currency === 'BTC') {
      // Bitcoin address validation
      const decoded = bitcoin.address.toOutputScript(address);
      return decoded.length > 0;

    } else if (['ETH', 'USDC', 'USDT'].includes(currency)) {
      // Ethereum address validation
      return ethers.isAddress(address);
    }

    return false;

  } catch (error) {
    return false;
  }
}

/**
 * Get wallet balance
 */
export async function getWalletBalance(currency: string): Promise<string> {
  if (currency === 'BTC') {
    return getBitcoinBalance();
  } else {
    return getEthereumBalance(currency);
  }
}

/**
 * Get Ethereum wallet balance
 */
async function getEthereumBalance(currency: string): Promise<string> {
  const provider = new ethers.JsonRpcProvider(process.env.ETHEREUM_RPC_URL!);
  const walletAddress = process.env.ETHEREUM_HOT_WALLET_ADDRESS!;

  if (currency === 'ETH') {
    const balance = await provider.getBalance(walletAddress);
    return ethers.formatEther(balance);

  } else {
    // ERC-20 token balance
    const tokenAddress = getTokenAddress(currency);
    const tokenContract = new ethers.Contract(
      tokenAddress,
      ['function balanceOf(address) view returns (uint256)'],
      provider
    );

    const balance = await tokenContract.balanceOf(walletAddress);
    const decimals = currency === 'USDC' || currency === 'USDT' ? 6 : 18;

    return ethers.formatUnits(balance, decimals);
  }
}

/**
 * Get Bitcoin wallet balance
 */
async function getBitcoinBalance(): Promise<string> {
  // Placeholder - implement actual Bitcoin balance check
  return '0.5'; // Mock balance
}

/**
 * Estimate network fees
 */
export async function estimateNetworkFee(
  currency: string,
  amount: string
): Promise<string> {
  if (currency === 'BTC') {
    // Bitcoin fee estimation
    // Use mempool.space API or similar
    return '0.0001'; // Mock fee

  } else {
    // Ethereum gas estimation
    const provider = new ethers.JsonRpcProvider(process.env.ETHEREUM_RPC_URL!);
    const gasPrice = await provider.getFeeData();

    if (currency === 'ETH') {
      const gasLimit = 21000n;
      const fee = gasPrice.gasPrice! * gasLimit;
      return ethers.formatEther(fee);

    } else {
      // ERC-20 transfer typically uses ~65000 gas
      const gasLimit = 65000n;
      const fee = gasPrice.gasPrice! * gasLimit;
      return ethers.formatEther(fee);
    }
  }
}

/**
 * Update transaction status in database
 */
async function updateTransactionStatus(
  transactionId: string,
  status: string,
  error?: string,
  txHash?: string
): Promise<void> {
  // Placeholder - implement actual database update
  console.log(`Updating transaction ${transactionId} to ${status}`, { error, txHash });
}

/**
 * Finalize transaction after confirmations
 */
async function finalizeTransaction(txHash: string): Promise<void> {
  // Placeholder - implement transaction finalization
  console.log(`Finalizing transaction: ${txHash}`);

  // Mark transaction as completed in database
  // Send confirmation email to user
  // Update analytics
}

/**
 * Handle failed transactions
 */
export async function handleFailedTransaction(
  transactionId: string,
  error: string
): Promise<void> {
  console.error(`Transaction ${transactionId} failed:`, error);

  // Update database
  await updateTransactionStatus(transactionId, 'failed', error);

  // Initiate refund if payment was captured
  // Send notification to user
  // Alert support team for manual review
}
