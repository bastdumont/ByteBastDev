import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Crypto Onramp - Buy Crypto with Stripe',
  description: 'Convert fiat currency to cryptocurrency using Stripe payments',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-blue-600">CryptoOnramp</h1>
              </div>
              <div className="flex items-center gap-4">
                <a href="/onramp" className="text-gray-700 hover:text-blue-600">Buy Crypto</a>
                <a href="/transactions" className="text-gray-700 hover:text-blue-600">Transactions</a>
              </div>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}
