import asyncio
from os import environ
from flask import Flask, request, jsonify
from pyrogram import Client, filters, idle

# Environment variables
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
SESSION = environ.get("SESSION")
TIME = int(environ.get("TIME"))
GROUPS = [int(grp) for grp in environ.get("GROUPS").split()]
ADMINS = [int(usr) for usr in environ.get("ADMINS").split()]

START_MSG = "<b>Hai {},\nI'm a private bot of @l_abani to delete group messages after a specific time</b>"

# Initialize Pyrogram clients
User = Client(name="user-account",
              session_string=SESSION,
              api_id=API_ID,
              api_hash=API_HASH,
              workers=300
              )

Bot = Client(name="auto-delete",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=300
             )

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
    app.run(host='0.0.0.0', port=5000)
    idle()

# Stop clients
async def stop_clients():
    await User.stop()
    print("User Stopped!")
    await Bot.stop()
    print("Bot Stopped!")

loop = asyncio.get_event_loop()
loop.run_until_complete(stop_clients())
