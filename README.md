# Telegram Appointment Bot

This repository contains a minimal example of a Telegram bot for managing hair salon appointments. The bot connects to a CalDAV calendar and allows customers to book or cancel appointments via Telegram.

## Setup

1. Install the required dependencies (Python 3.11+):
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.sample` to `.env` and fill in your credentials.
3. Run the bot:
   ```bash
   python3 main.py
   ```

## Files

- `main.py` – Entry point of the bot
- `bot_handlers.py` – Telegram command handlers and conversation flow
- `appointment_manager.py` – Logic for booking and cancelling appointments
- `caldav_manager.py` – CalDAV calendar integration

The existing `index.html` is unrelated to the bot and can be ignored.
