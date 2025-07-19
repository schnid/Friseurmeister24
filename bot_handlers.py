from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

from appointment_manager import AppointmentManager

CHOOSING_SERVICE, CHOOSING_DATE, CHOOSING_TIME, CONFIRMING = range(4)


def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    update.message.reply_text(
        "Hi, ich bin Clara – ich helfe dir beim Terminbuchen.\n"
        "Welche Leistung möchtest du?",
        reply_markup=ReplyKeyboardMarkup([
            ["Herrenhaarschnitt"],
            ["Farbe"],
            ["Strähnen"],
        ], one_time_keyboard=True, resize_keyboard=True),
    )
    return CHOOSING_SERVICE


def choose_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['service'] = update.message.text
    update.message.reply_text("Für welches Datum? (YYYY-MM-DD)", reply_markup=ReplyKeyboardRemove())
    return CHOOSING_DATE


def choose_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['date'] = update.message.text
    update.message.reply_text("Zu welcher Uhrzeit? (HH:MM)")
    return CHOOSING_TIME


def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['time'] = update.message.text
    service = context.user_data['service']
    date = context.user_data['date']
    time = context.user_data['time']
    update.message.reply_text(
        f"Du möchtest {service} am {date} um {time}. Bestätige mit 'ja'.")
    return CONFIRMING


def book(update: Update, context: ContextTypes.DEFAULT_TYPE, manager: AppointmentManager) -> int:
    if update.message.text.lower() != 'ja':
        update.message.reply_text("Buchung abgebrochen.")
        return ConversationHandler.END

    service = context.user_data['service']
    date = context.user_data['date']
    time = context.user_data['time']
    dt = datetime.fromisoformat(f"{date} {time}")
    booking_id = manager.book_appointment(service, dt)
    update.message.reply_text(
        f"Termin gebucht! Deine Buchungsnummer: {booking_id}")
    return ConversationHandler.END


def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    update.message.reply_text('Vorgang abgebrochen.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def setup_handlers(app: Application, manager: AppointmentManager) -> None:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_date)],
            CHOOSING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_time)],
            CHOOSING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
            CONFIRMING: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: book(u, c, manager))],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('cancel', cancel))
