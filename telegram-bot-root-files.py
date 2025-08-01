PK     W��Z��=�  �     main_bot.pyimport os
import smtplib
import random
from email.mime.text import MIMEText
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
ADMIN_USER_ID = int(os.environ.get("ADMIN_USER_ID", 0))

users = {}  # {telegram_id: {"email": ..., "verified": ..., "ref_by": ...}}

keyboard = [["Register", "Login"], ["Referral", "Logout"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def send_verification_code(to_email, code):
    msg = MIMEText(f"Your verification code is: {code}")
    msg["Subject"] = "Your Verification Code"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "Register":
        await update.message.reply_text("Enter your email:")
        context.user_data["state"] = "awaiting_email"
    elif text == "Login":
        await update.message.reply_text("Enter your email to login:")
        context.user_data["state"] = "login_email"
    elif text == "Referral":
        await update.message.reply_text(f"Your referral link: t.me/{context.bot.username}?start={user_id}")
    elif text == "Logout":
        users.pop(user_id, None)
        await update.message.reply_text("You have been logged out.")
    elif context.user_data.get("state") == "awaiting_email":
        email = text
        if email in [info["email"] for info in users.values()]:
            await update.message.reply_text("Email already registered.")
        else:
            code = str(random.randint(1000, 9999))
            context.user_data["verif_code"] = code
            context.user_data["email"] = email
            send_verification_code(email, code)
            context.user_data["state"] = "awaiting_code"
            await update.message.reply_text("Verification code sent to your email.")
    elif context.user_data.get("state") == "awaiting_code":
        if text == context.user_data.get("verif_code"):
            users[user_id] = {
                "email": context.user_data["email"],
                "verified": True,
                "ref_by": context.args[0] if context.args else None
            }
            await update.message.reply_text("Registration successful! Visit this bot for updates:
t.me/your_second_bot")
        else:
            await update.message.reply_text("Invalid code. Try again.")
    elif context.user_data.get("state") == "login_email":
        for uid, info in users.items():
            if info["email"] == text:
                await update.message.reply_text("Login successful!")
                return
        await update.message.reply_text("No account found. Please register.")
    else:
        await update.message.reply_text("Unknown command. Please use the menu.", reply_markup=markup)

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_USER_ID:
        user_list = "
".join([f"{uid}: {data['email']}" for uid, data in users.items()])
        await update.message.reply_text(f"Registered users:
{user_list or 'None'}")
    else:
        await update.message.reply_text("Unauthorized.")

def get_registered_data():
    return users

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
PK     W��Z(����  �     admin_panel.pyfrom flask import Flask, request
from main_bot import get_registered_data
import os

app = Flask(__name__)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

@app.route("/")
def home():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return "Unauthorized"
    users = get_registered_data()
    return "<br>".join([f"{uid}: {data['email']}" for uid, data in users.items()])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
PK     W��Zpg���   �      .env.exampleBOT_TOKEN=your_telegram_bot_token
SMTP_EMAIL=your_gmail_email
SMTP_PASSWORD=your_gmail_app_password
ADMIN_USER_ID=your_telegram_user_id
ADMIN_PASSWORD=your_flask_admin_password
PK     W��ZZ6�W<  <  	   README.md# Telegram Bot with Email Verification and Admin Panel

## 🛠 Technologies
- Python
- python-telegram-bot
- Flask (for admin panel)

## ⚙️ Environment Variables
- BOT_TOKEN
- SMTP_EMAIL
- SMTP_PASSWORD
- ADMIN_USER_ID
- ADMIN_PASSWORD

## 🚀 How to Deploy on Render

### Web Service:
- Start Command: `python admin_panel.py`
- Add `ADMIN_PASSWORD` in Environment

### Background Worker:
- Start Command: `python main_bot.py`
- Add the other variables (BOT_TOKEN, etc.)

Visit your admin panel with:
https://your-app-name.onrender.com/?password=your_admin_password
PK     W��Z�f�'   '      requirements.txtpython-telegram-bot==20.3
Flask==2.3.2
PK     W��Z��=�  �             ��    main_bot.pyPK     W��Z(����  �             ���  admin_panel.pyPK     W��Zpg���   �              ���  .env.examplePK     W��ZZ6�W<  <  	           ���  README.mdPK     W��Z�f�'   '              ��2  requirements.txtPK      $  �    