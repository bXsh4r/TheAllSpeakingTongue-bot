# TheAllSpeakingTongue-bot

A Telegram bot that specializes in translating user text.

# Features 
Users are allowed to choose any of the languages mentioned in languages.txt for the bot to translate from or to.

All user data is saved in an SQLite database in users.py.

# Functionality
The bot uses the Gemini API for translating the text. The text is sent to Gemini wrapped in a secured prompt that asks for precise translation. Then accepts the translated text and send it to the user.
