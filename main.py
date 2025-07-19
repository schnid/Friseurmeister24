import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bot_handlers import setup_handlers
from caldav_manager import CalDavManager
from appointment_manager import AppointmentManager


def main() -> None:
    """Start the Telegram bot."""
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    caldav_url = os.getenv("CALDAV_URL")
    caldav_user = os.getenv("CALDAV_USERNAME")
    caldav_pass = os.getenv("CALDAV_PASSWORD")

    caldav_manager = CalDavManager(caldav_url, caldav_user, caldav_pass)
    appointment_manager = AppointmentManager(caldav_manager)

    application = ApplicationBuilder().token(token).build()
    setup_handlers(application, appointment_manager)

    application.run_polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
