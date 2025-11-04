# Discord Bot

Feature-rich Discord bot with slash commands, database storage, and event handlers.

## Overview

Complete Discord bot featuring:
- **discord.py**: Discord API wrapper
- **Slash Commands**: Modern commands
- **Database**: Persistent storage
- **Cogs**: Modular commands
- **Error Handling**: Robust error handling

## Features

✅ **Commands**
- Slash commands
- Command groups
- Autocomplete
- Help system

✅ **Events**
- Message handling
- Reaction handling
- Member events
- Logging

✅ **Database**
- SQLite storage
- User profiles
- Server settings

✅ **Utilities**
- Permissions
- Cooldowns
- Validation

## Quick Start

### Prerequisites
```bash
Python >= 3.11
discord.py >= 2.3
```

### Installation

```bash
pip install -r requirements.txt
cp .env.example .env
python bot.py
```

## Project Structure

```
discord-bot/
├── bot.py               # Entry point
├── cogs/                # Command modules
│   ├── admin.py
│   ├── fun.py
│   └── utility.py
├── database.py          # Database setup
├── config.py            # Configuration
└── README.md
```

## Development

```bash
python bot.py           # Run bot
python -m pytest tests/ # Run tests
```

---

**Build amazing Discord bots!** 🤖
