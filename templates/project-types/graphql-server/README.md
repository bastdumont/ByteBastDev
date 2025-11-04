# GraphQL Server with Apollo

Production-ready GraphQL server with Apollo Server, PostgreSQL, Prisma ORM, and real-time subscriptions.

## Overview

A complete GraphQL server implementation featuring:
- **Apollo Server 4**: Modern GraphQL server
- **Prisma ORM**: Type-safe database access
- **PostgreSQL**: Robust database
- **Real-time**: Subscriptions support
- **Authentication**: JWT tokens
- **Validation**: Input validation
- **Documentation**: Apollo Studio integration

## Features

✅ **Full GraphQL Stack**
- Schema-first development
- Type safety with TypeScript
- Resolvers with proper typing
- Middleware support

✅ **Database**
- PostgreSQL integration
- Prisma migrations
- Data validation
- Connection pooling

✅ **Real-time Features**
- WebSocket subscriptions
- Live data updates
- Event-based architecture

✅ **Security**
- JWT authentication
- Field-level permissions
- Input validation
- Rate limiting ready

✅ **Development**
- Hot reload
- GraphQL Playground
- Apollo DevTools
- Error handling

## Quick Start

### Prerequisites
```bash
Node.js >= 18.0.0
npm >= 9.0.0
PostgreSQL >= 14
```

### Installation

```bash
npm install
cp .env.example .env
npx prisma migrate dev
npm run dev
```

### Access Apollo Studio
Open http://localhost:4000

## Project Structure

```
graphql-server/
├── src/
│   ├── schema.ts         # GraphQL schema
│   ├── resolvers/        # Resolver functions
│   ├── models/           # Prisma models
│   ├── middleware/       # Auth and validation
│   ├── utils/            # Helper functions
│   └── server.ts         # Apollo setup
├── prisma/
│   ├── schema.prisma    # Database schema
│   └── migrations/      # Migration files
├── .env.example
├── package.json
└── README.md
```

## API Examples

### Query

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    email
    name
    posts {
      id
      title
    }
  }
}
```

### Mutation

```graphql
mutation CreatePost($title: String!, $content: String!) {
  createPost(title: $title, content: $content) {
    id
    title
    createdAt
  }
}
```

### Subscription

```graphql
subscription OnPostCreated {
  postCreated {
    id
    title
    author {
      name
    }
  }
}
```

## Database Setup

### Initialize Database

```bash
npx prisma migrate dev --name init
npx prisma db seed
```

### Prisma Models

```prisma
model User {
  id        Int     @id @default(autoincrement())
  email     String  @unique
  name      String
  posts     Post[]
}

model Post {
  id        Int     @id @default(autoincrement())
  title     String
  content   String
  author    User    @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

## Configuration

### Environment Variables

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/graphql
NODE_ENV=development
JWT_SECRET=your-secret-key
APOLLO_KEY=your-apollo-key
PORT=4000
```

### Server Configuration

```typescript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({ user: req.user }),
  plugins: {
    willResolveField: () => {
      // Logging and metrics
    }
  }
});
```

## Development

### Running Server

```bash
npm run dev          # Start with hot reload
npm run start        # Production mode
npm run schema:push  # Push schema to Apollo
```

### Testing

```bash
npm run test         # Run tests
npm run test:watch   # Watch mode
```

### Database

```bash
npx prisma studio   # Visual database browser
npx prisma validate # Check schema
npx prisma format   # Format schema
```

## Deployment

### Build

```bash
npm run build
npm run generate    # Generate Prisma client
```

### Environment

Set production environment variables:
- `DATABASE_URL`: Production database
- `JWT_SECRET`: Secure random key
- `NODE_ENV`: production
- `APOLLO_KEY`: Apollo Studio key (optional)

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## Performance

### Optimization

- **DataLoader**: Batch loading to prevent N+1
- **Query Complexity**: Limit query depth
- **Pagination**: Cursor-based pagination
- **Caching**: Redis integration ready

### Monitoring

```typescript
// Performance tracking
apollo.plugin('willResolveField', async () => {
  const start = Date.now();
  return () => {
    console.log(`Field took ${Date.now() - start}ms`);
  };
});
```

## Security

### Best Practices

✅ Input validation with Zod  
✅ JWT authentication  
✅ CORS configuration  
✅ Rate limiting ready  
✅ SQL injection prevention (Prisma)  
✅ XSS protection  

### Authentication

```typescript
const context = async ({ req }) => {
  const token = req.headers.authorization?.split(' ')[1];
  const user = token ? verify(token, JWT_SECRET) : null;
  return { user };
};
```

## Troubleshooting

### Database Connection Error

```bash
# Check connection string
echo $DATABASE_URL

# Reset database
npx prisma migrate reset
```

### Port Already in Use

```bash
lsof -ti:4000 | xargs kill -9
```

### GraphQL Schema Error

```bash
npx prisma validate
npx prisma generate
```

## Resources

- [Apollo Documentation](https://www.apollographql.com/docs/)
- [Prisma Documentation](https://www.prisma.io/docs/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

---

**Ready to build your GraphQL API!** 🚀
