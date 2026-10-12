Telegram ID Lookup Bot

What it does
- Accepts a numeric Telegram user ID.
- Tries Telegram Bot API getChat for that ID.
- Displays the username and profile fields only if Telegram returns them.
- Handles unavailable profiles and API errors.

Important limitation
A numeric Telegram user ID alone does not guarantee that the bot can retrieve the user's profile or username. Telegram Bot API does not provide arbitrary-user phone-number lookup. The bot does not bypass privacy/access restrictions.

Setup
1. Create a bot with @BotFather and copy its token.
2. Install Python 3.10+.
3. Install dependencies:
   pip install -r requirements.txt
4. Set environment variable BOT_TOKEN to your bot token.
   Linux/macOS:
     export BOT_TOKEN="YOUR_BOT_TOKEN"
   Windows PowerShell:
     $env:BOT_TOKEN="YOUR_BOT_TOKEN"
5. Run:
   python bot.py

Deploying on a Python hosting service
- Upload bot.py and requirements.txt.
- Add environment variable BOT_TOKEN in the service's environment settings.
- Set the start command to: python bot.py
- Use a worker/background service if the host supports it; polling bots need a continuously running process.
