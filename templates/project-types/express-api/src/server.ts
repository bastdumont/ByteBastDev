import express, { Express } from 'express'
import cors from 'cors'
import helmet from 'helmet'
import compression from 'compression'
import cookieParser from 'cookie-parser'
import morgan from 'morgan'
import { config } from './config'
import { connectDB } from './config/database'
import { logger } from './utils/logger'
import { errorHandler } from './middleware/errorHandler'
import { rateLimiter } from './middleware/rateLimiter'
import routes from './routes'

const app: Express = express()

// Connect to database
connectDB()

// Middleware
app.use(helmet())
app.use(cors(config.cors))
app.use(compression())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(cookieParser())
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) } }))
app.use(rateLimiter)

// Routes
app.use('/api/v1', routes)

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  })
})

// Error handling
app.use(errorHandler)

// Start server
const PORT = config.port
app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT} in ${config.env} mode`)
})

export default app
