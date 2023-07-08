from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Update
from constants import API_KEY, OWNER_ID
import asyncio

async def start_command(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Leave a message by sending a message here!')


async def messageHandler(update, context):
    user_input = str(update.message.text)
    if update.effective_chat.id == OWNER_ID and ':' in user_input:
        msg_arr = user_input.split(':')
        id = int(msg_arr[0].strip())
        msg = ''.join(msg_arr[1:]).strip()
        # print(f"id: '{id}'\nmsg: '{msg}'")
        await context.bot.send_message(chat_id=id, text=msg)
        await update.message.reply_text('Message sent!')
        return
    await notify(update, context)
    await update.message.reply_text('Message sent!')


async def error(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="An exception has occurred!\n\nPlease inform the bot developer about this issue and the steps that caused it.")
    await context.bot.send_message(chat_id=OWNER_ID,
                                   text=f'ERROR:\n\nUpdate:\n {update}\n\ncaused error\n\nContext:\n{context.error}')
    # print(f'Update {update} caused error {context.error}')


def main():
    print('initializing bot..')
    app = ApplicationBuilder().token(API_KEY).build()
    asyncio.get_event_loop().run_until_complete(
        app.bot.send_message(chat_id=OWNER_ID, text="Bot started"))
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), messageHandler))
    app.add_error_handler(error)
    app.run_polling()


if __name__ == '__main__':
    main()
