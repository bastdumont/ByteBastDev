# Quick Start (5 Minutes)

Get ByteClaude up and running in just 5 minutes!

## Installation

### Step 1: Clone Repository (1 min)

```bash
git clone https://github.com/bastdumont/BalderFrameWork.git
cd BalderFrameWork
```

### Step 2: Install Dependencies (2 min)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or manually:
pip install PyYAML
```

### Step 3: Run Setup (1 min)

```bash
python setup.py
```

This creates necessary directories and verifies configuration.

### Step 4: Verify Installation (30 sec)

```bash
python orchestrator/main.py --version
```

✅ You're ready!

## Your First Project (5 Minutes)

### Option A: Interactive Mode

```bash
python orchestrator/main.py
```

You'll see:

```
╔════════════════════════════════════════════════════════════╗
║          Welcome to ByteClaude Framework                   ║
║    Automated AI-Powered Development Environment            ║
╚════════════════════════════════════════════════════════════╝

📝 Describe what you want to build: Create a React to-do app

[Framework analyzes and creates a plan...]

Tasks to execute:
1. Setup project structure
2. Fetch React documentation
3. Generate components
4. Create tests
5. Generate documentation

Execute? (y/n): y
```

The framework will:
- ✅ Create project structure
- ✅ Fetch documentation
- ✅ Generate code
- ✅ Create tests
- ✅ Generate README

All in 2-3 minutes!

### Option B: Direct Command

```bash
python orchestrator/main.py \
  --task "Create a React to-do app" \
  --output-dir ./my-todo-app

cd output/my-todo-app
npm install
npm start
```

## What Gets Created

After execution, you'll have:

```
output/my-todo-app/
├── README.md                 # Complete documentation
├── package.json             # Dependencies configured
├── src/
│   ├── App.tsx             # Main component
│   ├── components/         # React components
│   ├── hooks/              # Custom hooks
│   └── utils/              # Utilities
├── tests/
│   └── App.test.tsx        # Test suite
└── execution_report.json   # Detailed execution log
```

## Next Steps

### 1. Explore Examples
```bash
cat examples/USAGE_EXAMPLES.md
```

### 2. Read Architecture
```bash
cat ARCHITECTURE.md
```

### 3. Try a Complex Project
```bash
python orchestrator/main.py \
  --task "Create a Next.js SaaS with Stripe and MongoDB" \
  --include-tests
```

### 4. Customize Configuration
Edit `config/framework-config.yaml`:
- Increase parallel tasks
- Adjust cache settings
- Configure validation

## Common Tasks

### Create a Web App
```bash
python orchestrator/main.py \
  --task "Create a React dashboard with Tailwind CSS"
```

### Build an API
```bash
python orchestrator/main.py \
  --task "Create a FastAPI backend with MongoDB"
```

### Generate Documents
```bash
python orchestrator/main.py \
  --task "Generate PDF invoice from MongoDB data"
```

### Build Full Stack
```bash
python orchestrator/main.py \
  --task "Create full-stack app: Next.js frontend + FastAPI backend + MongoDB"
```

## Troubleshooting

### Issue: Command not found
```bash
# Make sure you're in the ByteClaude directory
cd /path/to/BalderFrameWork

# Try with python3 explicitly
python3 orchestrator/main.py
```

### Issue: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Permission denied
```bash
# Make scripts executable
chmod +x setup.py
chmod +x orchestrator/main.py
```

## Key Resources

- 📚 **[Getting Started Guide](installation.md)** - Detailed setup
- 🏗️ **[Architecture](../core-concepts/architecture.md)** - How it works
- 💡 **[Examples](../examples/quick-examples.md)** - Real-world usage
- ⚙️ **[Configuration](configuration.md)** - Customize settings
- 🐛 **[Troubleshooting](../troubleshooting/common-issues.md)** - Problem solving

## Performance Tips

### Speed Up Execution
1. **Increase parallelism**
   ```yaml
   framework:
     max_parallel_tasks: 10
   ```

2. **Extend cache TTL**
   ```yaml
   context7:
     cache_ttl: 7200  # 2 hours
   ```

3. **Disable tests for speed**
   ```bash
   python orchestrator/main.py --task "..." --skip-tests
   ```

## What's Happening Behind the Scenes

When you run a task, ByteClaude:

1. **Analyzes** your request
2. **Detects** technologies needed
3. **Fetches** current documentation
4. **Plans** execution sequence
5. **Executes** tasks (in parallel where possible)
6. **Validates** output quality
7. **Generates** documentation

All with automatic error handling and retries!

## Next: Build Something Real

Ready? Try one of these:

```bash
# SaaS Startup
python orchestrator/main.py --task "Next.js SaaS with Stripe payments"

# Business Dashboard
python orchestrator/main.py --task "React admin dashboard with data viz"

# Data Processing
python orchestrator/main.py --task "Python ETL pipeline with Airflow"

# API Service
python orchestrator/main.py --task "FastAPI with MongoDB and JWT auth"
```

---

**Congratulations!** 🎉 You're ready to build with ByteClaude.

For detailed information, see [Installation Guide](installation.md).

