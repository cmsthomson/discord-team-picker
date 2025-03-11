# Discord Team Picker Bot

A simple Discord bot that organizes players into random teams for **ARAM** and **Arena** game modes.

## Features

- Automatically detects members in a voice channel
- Supports adding and removing members before starting
- Creates balanced teams for **ARAM** (max 5 per team) and **Arena** (2 per team)
- Supports rematching with shuffled teams

## Commands

- `!start_game` - Starts a new game session
- `!rematch` - Randomizes teams again without selecting a new game mode
- `!list` - Lists the current members in the pool

## Installation

1. Clone the repository:
```console
   git clone https://github.com/cmsthomson/discord-team-picker.git
   cd discord-game-bot
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```   
3. Set up your bot token in a `.env` file:
```text
   DISCORD_TOKEN=your-bot-token-here
```
4. Run the bot:
```bash
   python bot.py
```
