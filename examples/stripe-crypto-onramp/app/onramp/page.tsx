'use client';

export default function OnrampPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h1 className="text-3xl font-bold mb-6">Buy Cryptocurrency</h1>

          <div className="mb-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-blue-800">
              ℹ️ <strong>Demo Mode:</strong> This is a demonstration application.
              To run with real payments, you need to:
            </p>
            <ul className="list-disc list-inside mt-2 text-sm text-blue-700">
              <li>Set up a Stripe account and add API keys</li>
              <li>Configure a PostgreSQL database</li>
              <li>Set up Redis for caching</li>
              <li>Configure blockchain RPC endpoints</li>
              <li>Add all required environment variables from .env.example</li>
            </ul>
          </div>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Amount to Buy
              </label>
              <div className="flex gap-2">
                <input
                  type="number"
                  placeholder="100"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled
                />
                <select className="px-4 py-3 border border-gray-300 rounded-lg" disabled>
                  <option>USD</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cryptocurrency
              </label>
              <select className="w-full px-4 py-3 border border-gray-300 rounded-lg" disabled>
                <option>ETH - Ethereum</option>
                <option>BTC - Bitcoin</option>
                <option>USDC - USD Coin</option>
                <option>USDT - Tether</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Wallet Address
              </label>
              <input
                type="text"
                placeholder="0x..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled
              />
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Exchange Rate:</span>
                <span className="font-semibold">--</span>
              </div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">You'll Receive:</span>
                <span className="font-semibold">--</span>
              </div>
              <div className="border-t border-gray-300 my-2"></div>
              <div className="flex justify-between text-sm text-gray-500 mb-1">
                <span>Stripe Fee:</span>
                <span>--</span>
              </div>
              <div className="flex justify-between text-sm text-gray-500 mb-1">
                <span>Platform Fee:</span>
                <span>--</span>
              </div>
              <div className="flex justify-between text-sm text-gray-500">
                <span>Network Fee:</span>
                <span>--</span>
              </div>
            </div>

            <button
              disabled
              className="w-full bg-gray-300 text-gray-600 py-3 px-4 rounded-lg font-semibold cursor-not-allowed"
            >
              Configure Environment to Enable
            </button>

            <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h3 className="font-semibold text-yellow-800 mb-2">Setup Instructions:</h3>
              <ol className="list-decimal list-inside text-sm text-yellow-700 space-y-1">
                <li>Copy .env.example to .env.local</li>
                <li>Add your Stripe API keys</li>
                <li>Set up PostgreSQL and add DATABASE_URL</li>
                <li>Run: npm install</li>
                <li>Run: npx prisma migrate dev</li>
                <li>Run: npm run dev</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
