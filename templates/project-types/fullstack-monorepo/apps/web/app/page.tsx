'use client'

import { useState, useEffect } from 'react'
import { Button } from 'ui'

interface ApiResponse {
  message: string
  timestamp: string
}

export default function HomePage() {
  const [data, setData] = useState<ApiResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchFromAPI = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/v1/health')
      if (!response.ok) throw new Error('API request failed')

      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchFromAPI()
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Full-Stack Monorepo
        </h1>

        <p className="text-center mb-8 text-gray-600">
          Next.js Frontend + FastAPI Backend
        </p>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold mb-4">API Connection</h2>

          {loading && (
            <p className="text-blue-500">Loading...</p>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded">
              <p className="font-semibold">Error:</p>
              <p>{error}</p>
              <p className="text-sm mt-2">Make sure the API is running on port 8000</p>
            </div>
          )}

          {data && (
            <div className="bg-green-50 border border-green-200 p-4 rounded">
              <p className="font-semibold text-green-700">✓ Connected to API</p>
              <p className="text-sm text-gray-600 mt-2">
                Message: {data.message}
              </p>
              <p className="text-sm text-gray-600">
                Time: {new Date(data.timestamp).toLocaleString()}
              </p>
            </div>
          )}

          <Button
            onClick={fetchFromAPI}
            className="mt-4"
            disabled={loading}
          >
            {loading ? 'Refreshing...' : 'Refresh API Status'}
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border rounded-lg p-6">
            <h3 className="font-semibold text-lg mb-2">Frontend</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>✓ Next.js 14</li>
              <li>✓ React 18</li>
              <li>✓ TypeScript</li>
              <li>✓ Tailwind CSS</li>
              <li>✓ Shared UI components</li>
            </ul>
          </div>

          <div className="border rounded-lg p-6">
            <h3 className="font-semibold text-lg mb-2">Backend</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>✓ FastAPI</li>
              <li>✓ Python 3.11+</li>
              <li>✓ Async/await</li>
              <li>✓ Auto API docs</li>
              <li>✓ CORS enabled</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  )
}
