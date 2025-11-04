# Next.js SaaS Starter

A production-ready SaaS boilerplate built with Next.js 14, TypeScript, Tailwind CSS, Stripe, and NextAuth.js.

## Features

- ✅ **Next.js 14** with App Router
- ✅ **TypeScript** for type safety
- ✅ **Tailwind CSS** for styling
- ✅ **NextAuth.js** for authentication (email/password, Google, GitHub)
- ✅ **Prisma** ORM with PostgreSQL
- ✅ **Stripe** integration for subscriptions and payments
- ✅ **Responsive design** with dark mode support
- ✅ **Landing page** with hero, features, pricing sections
- ✅ **User dashboard** with subscription management
- ✅ **Admin panel** for user management
- ✅ **Email notifications** with Nodemailer
- ✅ **SEO optimized** with metadata API

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- PostgreSQL database
- Stripe account
- (Optional) Google OAuth credentials
- (Optional) GitHub OAuth credentials

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd {{project_name}}
```

2. Install dependencies:
```bash
npm install
```

3. Copy the environment variables:
```bash
cp .env.example .env
```

4. Update the `.env` file with your credentials:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
NEXTAUTH_SECRET="your-secret-key"
STRIPE_API_KEY="sk_test_..."
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_test_..."
# Add other credentials as needed
```

5. Set up the database:
```bash
npx prisma generate
npx prisma db push
```

6. (Optional) Seed the database:
```bash
npm run db:seed
```

7. Start the development server:
```bash
npm run dev
```

8. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
├── app/                    # Next.js app directory
│   ├── (auth)/            # Authentication routes
│   ├── (dashboard)/       # Protected dashboard routes
│   ├── (marketing)/       # Public marketing routes
│   ├── api/               # API routes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── auth/             # Authentication components
│   ├── dashboard/        # Dashboard components
│   └── marketing/        # Marketing components
├── lib/                   # Utility libraries
│   ├── db.ts             # Prisma client
│   ├── auth.ts           # NextAuth configuration
│   ├── stripe.ts         # Stripe utilities
│   └── email.ts          # Email utilities
├── prisma/               # Prisma schema and migrations
│   └── schema.prisma     # Database schema
└── config/               # Configuration files
    ├── site.ts           # Site configuration
    └── subscriptions.ts  # Subscription plans
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run db:push` - Push Prisma schema to database
- `npm run db:studio` - Open Prisma Studio
- `npm run db:generate` - Generate Prisma client
- `npm run db:migrate` - Run database migrations
- `npm run db:seed` - Seed the database
- `npm run stripe:listen` - Listen to Stripe webhooks locally

## Stripe Setup

### 1. Create Products and Prices

In your Stripe Dashboard:
1. Go to Products
2. Create three products: Starter, Pro, Enterprise
3. For each product, create a recurring price
4. Copy the price IDs and add them to your `.env` file

### 2. Set up Webhooks

For local development:
```bash
npm run stripe:listen
```

For production:
1. Go to Stripe Dashboard > Developers > Webhooks
2. Add endpoint: `https://yourdomain.com/api/webhooks/stripe`
3. Select events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
4. Copy the webhook secret to your `.env` file

## Authentication Setup

### Email/Password

Email/password authentication works out of the box. Users can register and login with their credentials.

### OAuth Providers

#### Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:3000/api/auth/callback/google`
6. Copy Client ID and Client Secret to `.env`

#### GitHub OAuth

1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Create a new OAuth App
3. Set Authorization callback URL: `http://localhost:3000/api/auth/callback/github`
4. Copy Client ID and Client Secret to `.env`

## Database Schema

The application uses the following database models:

- **User** - User accounts
- **Account** - OAuth accounts
- **Session** - User sessions
- **VerificationToken** - Email verification tokens
- **Subscription** - User subscriptions

## Customization

### Site Configuration

Edit `config/site.ts` to customize:
- Site name and description
- Navigation links
- Social media links
- Contact information

### Subscription Plans

Edit `config/subscriptions.ts` to customize:
- Plan names and descriptions
- Pricing
- Features
- Stripe price IDs

### Styling

The project uses Tailwind CSS with a custom design system:
- Colors: Edit in `tailwind.config.ts` and `app/globals.css`
- Components: Modify components in `components/ui/`
- Layout: Update layout components

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy

### Other Platforms

The application can be deployed to any platform that supports Node.js:
- Railway
- Render
- AWS
- Digital Ocean
- etc.

Make sure to:
1. Set all environment variables
2. Run database migrations
3. Set up Stripe webhooks for your production URL

## Security Considerations

- ✅ Environment variables are used for secrets
- ✅ Passwords are hashed with bcrypt
- ✅ CSRF protection with NextAuth.js
- ✅ API routes are protected with authentication
- ✅ Database queries use Prisma for SQL injection protection
- ✅ Stripe webhooks are verified

## Support

For issues and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## License

MIT License - feel free to use this boilerplate for your projects.

## Credits

Built with:
- [Next.js](https://nextjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Prisma](https://www.prisma.io/)
- [NextAuth.js](https://next-auth.js.org/)
- [Stripe](https://stripe.com/)
- [Radix UI](https://www.radix-ui.com/)
