from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from json import loads
from telegram import ReplyKeyboardMarkup

token = '1188178965:AAHr8WXr5AsFRS_v62IDHnWi_3kDj5oN0oc'

data = loads(open('past_matches.json', 'r').read())

users = {}

games = list(set([i['game'] for i in data])) + ['CS GO', 'Все игры']

keyboard = ReplyKeyboardMarkup([[i] for i in games], True, False)


def key(x):
    return x['date']


def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Привет! Спроси меня о результатах матчей!", reply_markup=keyboard)


def answer(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text

    if text == 'Все игры':
        users.pop(chat_id)
        context.bot.send_message(chat_id, 'Включен фильтр: Все игры', reply_markup=keyboard)
        return
    if text in games:
        users[chat_id] = text
        context.bot.send_message(chat_id, 'Включен фильтр: ' + text, reply_markup=keyboard)
        return

    new_data = data
    if chat_id in users:
        new_data = [i for i in data if i['game'] == users[chat_id]]
    selected = sorted([i for i in new_data if i['first_team'].replace(' ', '') == text.replace(' ', '') or i['second_team'].replace(' ', '') == text.replace(' ', '')], key=key)
    if not selected:
        context.bot.send_message(chat_id, "Такой команды не найдено", reply_markup=keyboard)
    else:
        n = min(3, len(selected))
        mes = ''
        for i in range(n):
            cur = selected[i]
            if cur['results']:
                mes += cur['date_real'] + ' | <u><i><b>' + cur['first_team'] + '</b></i></u> | ' + \
                       cur['second_team'] + ' | ' + cur['id'] + '\n'
            else:
                mes += cur['date_real'] + ' | ' + cur['first_team'] + ' | <u><i><b>' + \
                       cur['second_team'] + '</b></i></u> | ' + cur['id'] + '\n'
        context.bot.send_message(chat_id, mes, parse_mode='html', reply_markup=keyboard)


if __name__ == '__main__':
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    mes_handler = MessageHandler(Filters.text, answer)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(mes_handler)
    updater.start_polling()
