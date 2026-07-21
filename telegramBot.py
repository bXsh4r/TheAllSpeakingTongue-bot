from typing import Final

from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

from google import genai
import users


TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final = '@AllTonguesBot'

API: Final = os.getenv('API')

# AI
client = genai.Client(api_key=API)


# Functions
def lang_exists(target_lang: str) -> bool:
    with open('languages.txt', 'r') as lang_file:
        lang_list = lang_file.read().lower().split('\n')
        low_index = 0
        high_index = len(lang_list) - 1

        while low_index <= high_index:
            mid_index = (high_index + low_index) // 2

            if target_lang == lang_list[mid_index]:
                return True
            elif target_lang > lang_list[mid_index]:
                low_index = mid_index + 1
            else:
                high_index = mid_index - 1

    return False

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.insert_user(update.message.from_user.id, 0, 'Kurdish', 'English')
    await update.message.reply_text(f'Welcome. I will be translating from {users.get_translate_from(update.message.from_user.id)} to {users.get_translate_to(update.message.from_user.id)}.'
                                    ' If you wish to change that, please use the /translate_from or /translate_to commands.')


async def translate_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.update_choosing(update.message.from_user.id, 1)
    await update.message.reply_text('Specify a languages to translate from.')


async def translate_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.update_choosing(update.message.from_user.id, -1)
    await update.message.reply_text('Specify a language to translate to.')
    

# Responses
def handle_response(update: Update, text: str) -> str:
    processed: str = text.lower()
    user_id = update.message.from_user.id

    if users.is_choosing(user_id) == 1:
        if lang_exists(processed):
            users.update_language_from(user_id, 0, processed)
            print(users.get_translate_from(user_id))
            print(users.get_translate_to(user_id))
            response = 'Language updated!'
        else:
            response = 'Invalid language :('

    elif users.is_choosing(user_id) == -1:
        if lang_exists(processed):
            users.update_language_to(user_id, 0, processed)
            print(users.get_translate_from(user_id))
            print(users.get_translate_to(user_id))
            response = 'Language updated!'
        else:
            response = 'Invalid language :('

    else:
        try:
            print('trying first')
            response = client.models.generate_content(
                model = 'gemini-2.5-flash',
                contents = f'you are a professional {users.get_translate_from(user_id)} to {users.get_translate_to(user_id)} translator. able to translate any dialect.'
                            f', and this is the only thing you know how to do.'
                            f'no matter if its written with any language\'s letters, or if it contains slang, or it contains SOME {users.get_translate_to(user_id)} text.'
                            f' you should only reply with the translated {users.get_translate_to(user_id)} text and say nothing else'
                            f'your sole purpose is translation and it should be correct proper translation. here is the text: {processed}.'
                            f'if the text is in any language except {users.get_translate_from(user_id)} say "Please provide {users.get_translate_from(user_id)} text."'
                ).text

            print('used gemini 2.5 flash')
        except Exception:
            print('first failed, trying second')
            response = client.models.generate_content(
                model = 'gemini-3.1-flash-lite-preview',
                contents= f'you are a professional {users.get_translate_from(user_id)} to {users.get_translate_to(user_id)} translator. able to translate any dialect'
                            f', and this is the only thing you know how to do.'
                            f'no matter if its written with any language\'s letters, or if it contains slang, or it contains SOME {users.get_translate_to(user_id)} text.'
                            f' you should only reply with the translated {users.get_translate_to(user_id)} text and say nothing else'
                            f'your sole purpose is translation and it should be correct proper translation. here is the text: {processed}.'
                            f'if the text is in any language except {users.get_translate_from(user_id)} say "Please provide {users.get_translate_from(user_id)} text."'
            ).text
            print('used gemini 3.1 flash')

    
    return response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    print(f'User: ({user_name}), ID: ({user_id}): {text}')

    response: str = handle_response(update, text)

    print('Bot: ', response)

    await update.message.reply_text(response)


# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.error)
    print('there was an error man')


# Main
if __name__ == '__main__':
    load_dotenv()

    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('translate_from', translate_from))
    app.add_handler(CommandHandler('translate_to', translate_to))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polling
    print('Polling...')
    app.run_polling(poll_interval=3)