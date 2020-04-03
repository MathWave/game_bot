from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from json import loads


token = '1188178965:AAHr8WXr5AsFRS_v62IDHnWi_3kDj5oN0oc'

data = loads(open('past_matches.json', 'r').read())


def key(x):
    return x['date']


def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Привет! Спроси меня о результатах матчей!")


def answer(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    selected = sorted([i for i in data if i['first_team'] == text or i['second_team'] == text], key=key)
    if not selected:
        context.bot.send_message(chat_id, "Такой команды не найдено")
    else:
        n = min(3, len(selected))
        mes = ''
        for i in range(n):
            cur = selected[i]
            if cur['results']:
                mes += cur['date'] + ' | <u><i><b>' + cur['first_team'] + '</b></i></u> | ' + \
                       cur['second_team'] + ' | ' + cur['id'] + '\n'
            else:
                mes += cur['date'] + ' | ' + cur['first_team'] + ' | <u><i><b>' + \
                       cur['second_team'] + '</b></i></u> | ' + cur['id'] + '\n'
        context.bot.send_message(chat_id, mes, parse_mode='html')


if __name__ == '__main__':
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    mes_handler = MessageHandler(Filters.text, answer)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(mes_handler)
    updater.start_polling()