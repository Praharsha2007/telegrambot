import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ----------- Quotes & Categories -----------
local_quotes = [
    "Believe in yourself and all that you are.",
    "Every day is a new chance to grow.",
    "Push harder than yesterday if you want a different tomorrow.",
    "Small steps every day lead to big results.",
    "Your only limit is your mind.",
    "Be stronger than your excuses.",
    "You are capable of amazing things.",
    "Progress, not perfection.",
    "You didn’t come this far to only come this far.",
    "Great things never come from comfort zones."
]

categories = {
    "study": [
        "Study now, shine later.",
        "Push yourself — no one else will do it for you.",
        "The expert in anything was once a beginner.",
        "Wake up with determination, go to bed with satisfaction.",
        "Success doesn’t come to you — you go to it.",
        "Focus on progress, not perfection.",
        "Learning is never done without errors and defeat.",
        "Dream big, study hard, stay humble.",
        "Don’t wish for it. Work for it.",
        "Discipline is the bridge between goals and success."
    ],
    "success": [
        "Success is built daily.",
        "Dream big. Work hard. Stay focused.",
        "Your future is created by what you do today.",
        "Don’t watch the clock; do what it does — keep going.",
        "Action is the foundational key to all success.",
        "If you want to fly, give up everything that weighs you down.",
        "Success doesn’t just find you — you have to go out and get it.",
        "The harder you work for something, the greater you’ll feel when you achieve it.",
        "Doubt kills more dreams than failure ever will.",
        "Stay patient and trust your journey."
    ],
    "gym": [
        "Don’t stop when you’re tired. Stop when you’re done.",
        "Train hard, stay humble.",
        "Sweat is just fat crying.",
        "Your body can stand almost anything — it’s your mind you have to convince.",
        "No pain, no gain.",
        "When you feel like quitting, remember why you started.",
        "The only bad workout is the one you didn’t do.",
        "Strong mind. Strong body.",
        "Push yourself because no one else is going to do it for you.",
        "You don’t have to be extreme, just consistent."
    ],
    "confidence": [
        "Believe you can and you're halfway there.",
        "Confidence is the best outfit. Rock it and own it!",
        "You are stronger than you think.",
        "Don’t let anyone dull your sparkle.",
        "Trust yourself — you’ve survived a lot, and you’ll survive whatever’s next.",
        "You are enough just as you are.",
        "Stop doubting yourself, work hard, and make it happen.",
        "Be proud of how far you’ve come.",
        "You have within you right now everything you need to deal with whatever the world throws at you.",
        "Believe in your infinite potential."
    ]
}

# ----------- Helper Functions -----------
def get_api_quote():
    """Fetch a quote from ZenQuotes API"""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = response.json()
        return f"{data[0]['q']} — {data[0]['a']}"
    except Exception:
        return random.choice(local_quotes)

# ----------- Command Handlers -----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the Motivational Bot!\n\n"
        "Type /category to choose your motivation type or get started!"
    )

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌟 Random Quote", callback_data="random")],
        [InlineKeyboardButton("📚 Study", callback_data="study"),
         InlineKeyboardButton("💪 Gym", callback_data="gym")],
        [InlineKeyboardButton("🏆 Success", callback_data="success"),
         InlineKeyboardButton("🔥 Confidence", callback_data="confidence")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click a button to get your motivational quote:",
        reply_markup=reply_markup
    )

# ----------- Inline Button Handler -----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data in ["random", "study", "success", "gym", "confidence"]:
        # Pick a quote
        if data == "random":
            quote = get_api_quote()
        else:
            quote = random.choice(categories.get(data, local_quotes))

        # After quote, ask for next action
        keyboard = [
            [InlineKeyboardButton("✨ Another Quote", callback_data=data)],
            [InlineKeyboardButton("❌ Exit", callback_data="exit")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=f"{quote}\n\nWould you like another one?", reply_markup=reply_markup)

    elif data == "exit":
        await query.edit_message_text("Thanks for using the Motivational Bot! 🌟 Type /category anytime to get more quotes!")

# ----------- Message Handler -----------
async def quote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = get_api_quote()
    keyboard = [
        [InlineKeyboardButton("✨ Another Quote", callback_data="random")],
        [InlineKeyboardButton("❌ Exit", callback_data="exit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"{quote}\n\nWould you like another one?", reply_markup=reply_markup)

# ----------- Main Function -----------
def main():
    TOKEN = "8089546800:AAF4lNnboVR5T2sRipRL3tz3J7tuy3tyDok"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("category", category))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, quote_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
