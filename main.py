import asyncio
from flask import Flask, request, jsonify
from pyrogram import Client, filters, idle
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION = os.getenv("SESSION")
TIME = int(os.getenv("TIME"))
GROUPS = [int(grp) for grp in os.getenv("GROUPS").split()]
ADMINS = [int(usr) for usr in os.getenv("ADMINS").split()]

START_MSG = "<b>Hai {},\nI'm a private bot of @l_abani to delete group messages after a specific time</b>"

# Initialize Pyrogram clients
User = Client(name="user-account",
              session_string=SESSION,
              api_id=API_ID,
              api_hash=API_HASH,
              workers=300)

Bot = Client(name="auto-delete",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=300)

# Initialize Flask app
app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "running"})

@app.route('/restart', methods=['POST'])
def restart():
    # This is a simple restart endpoint
    return jsonify({"status": "restarting"}), 200

# Pyrogram Handlers
@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(START_MSG.format(message.from_user.mention))

@User.on_message(filters.chat(GROUPS))
async def delete(user, message):
    try:
        if message.from_user.id in ADMINS:
            return
        else:
            await asyncio.sleep(TIME)
            await Bot.delete_messages(message.chat.id, message.id)
    except Exception as e:
        print(e)

# Start clients and Flask app
async def start_clients():
    await User.start()
    print("User Started!")
    await Bot.start()
    print("Bot Started!")

@app.before_first_request
def before_first_request():
    loop = asyncio.get_event_loop()
    loop.create_task(start_clients())

@app.after_request
def after_request(response):
    # Handle cleanup if necessary
    return response

if __name__ == '__main__':
    from threading import Thread

    # Run Flask app in a separate thread
    def run_flask():
        app.run(host='0.0.0.0', port=5000)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the asyncio event loop
    asyncio.get_event_loop().run_forever()
  
