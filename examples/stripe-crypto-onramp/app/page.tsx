export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Buy Crypto with Stripe
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Convert fiat currency to cryptocurrency instantly and securely
          </p>
          <a
            href="/onramp"
            className="inline-block bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
          >
            Get Started
          </a>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="text-4xl mb-4">💳</div>
            <h3 className="text-xl font-semibold mb-2">Easy Payments</h3>
            <p className="text-gray-600">
              Pay with credit card, debit card, or bank transfer via Stripe
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="text-4xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold mb-2">Secure</h3>
            <p className="text-gray-600">
              PCI-DSS compliant with industry-leading security standards
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold mb-2">Fast</h3>
            <p className="text-gray-600">
              Receive your crypto in 10-30 minutes after payment confirmation
            </p>
          </div>
        </div>

        {/* Supported Cryptocurrencies */}
        <div className="bg-white rounded-xl shadow-md p-8">
          <h2 className="text-2xl font-bold text-center mb-8">Supported Cryptocurrencies</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { name: 'Bitcoin', symbol: 'BTC', icon: '₿' },
              { name: 'Ethereum', symbol: 'ETH', icon: 'Ξ' },
              { name: 'USDC', symbol: 'USDC', icon: '$' },
              { name: 'Tether', symbol: 'USDT', icon: '₮' },
            ].map((crypto) => (
              <div key={crypto.symbol} className="text-center p-4 border border-gray-200 rounded-lg hover:border-blue-500 transition">
                <div className="text-3xl mb-2">{crypto.icon}</div>
                <div className="font-semibold">{crypto.name}</div>
                <div className="text-sm text-gray-500">{crypto.symbol}</div>
              </div>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-16">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { step: '1', title: 'Enter Amount', desc: 'Choose how much crypto you want to buy' },
              { step: '2', title: 'Add Wallet', desc: 'Enter your cryptocurrency wallet address' },
              { step: '3', title: 'Pay', desc: 'Complete payment securely with Stripe' },
              { step: '4', title: 'Receive', desc: 'Get crypto sent directly to your wallet' },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="font-semibold mb-2">{item.title}</h3>
                <p className="text-sm text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 bg-blue-600 rounded-xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to get started?</h2>
          <p className="text-xl mb-8 opacity-90">
            Start buying cryptocurrency today with just a few clicks
          </p>
          <a
            href="/onramp"
            className="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition"
          >
            Buy Crypto Now
          </a>
        </div>
      </div>
    </div>
  )
}
