import telebot
import json
import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dataBase import Database

database = Database()

bot = telebot.TeleBot('5378702776:AAEvxu4UJzndPxnxY8sbxDvaZFJW4iMU3a8')

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    sti1 = 'CAACAgIAAxkBAAEFNlhixrMoXTQAAcV4DmIcJusAATcOGedTAAJREQACdQN4Sws8c6r43ZGvKQQ'
    print(call.message.text)
    req = call.data.split('_')

    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_sticker(call.message.chat.id, sti1)
    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']
        if 'Азия 🌏' in call.message.text:
            title = 'Азия 🌏'
            table = 'organization2'
        elif 'США 🇺🇸' in call.message.text:
            title = 'США 🇺🇸'
            table = 'organization'
        elif 'Канада 🇨🇦' in call.message.text:
            title = 'Канада 🇨🇦'
            table = 'organization3'
        else:
             table = 'organization'
        sqlTransaction = database.listColledjeForPage(tables=table, order='name', Page=page,
                                                      SkipSize=1)
        
        data = sqlTransaction[0][0]
        count = sqlTransaction[2]

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        if page == 1:
            markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд ->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) + "}"))
        elif page == count:
            markup.add(InlineKeyboardButton(text=f'<- Назад',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
        else:
            markup.add(InlineKeyboardButton(text=f'<- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page-1) + ",\"CountPage\":" + str(count) + "}"),
                           InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                           InlineKeyboardButton(text=f'Вперёд ->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))
        bot.edit_message_text(f'<b>{title}</b>\n\n'
                                    f'<b>{data[3]}</b>\n\n'
                                    f'<b>{data[1]}</b>\n\n'
                                    f'<b>Стоимость обучения:</b><i>{data[5]}</i>\n'
                                    f'<b>Максимальный грант:</b><i>{data[7]}</i>\n'
                                    f'<b>Сайт университета:</b><i>{data[2]}</i>\n'
                                    f'<b>Требуемые результаты SAT/IELTS:</b><i>{data[6]}</i>\n'
                                    f'<b>Дедлайн подачи заявок:</b><i> {data[4]}</i>',
                                    parse_mode="HTML",reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)










@bot.message_handler(commands=['start'])
def start(message):
    sti2 = 'CAACAgIAAxkBAAEFQ5pizxlO4AiqjTiYKvAsmBbVJJxilwACxhEAAviHcUkP4R-vYKNcHikE'
    bot.send_sticker(message.chat.id, sti2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Совет 🌥")
    btn2 = types.KeyboardButton("Бакалавр 🎓")
    btn3 = types.KeyboardButton("Образовательные центры 🏫")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Добро пожаловать, {0.first_name}!💗\nВыберите интересующий Вас пункт:".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Совет 🌥"):
        bot.send_message(message.chat.id, text= """ Набери следующие результаты: 
Идеальный результат:
· IELTS – выше 7.5 баллов
· TOEFL - выше 100 баллов
· SAT - выше 1500 баллов

Отличный результат:
· IELTS – 7.0 баллов
· TOEFL - 100 баллов
· SAT - 1450-1500 баллов

Хороший результат
· IELTS – 6.5 баллов
· TOEFL - 90-100 баллов
· SAT - 1400-1450 баллов

Нормальный результат:
· IELTS – 6.0баллов
· TOEFL - 80-90 баллов
· SAT - 1300-1400 баллов """)

    elif(message.text == "Бакалавр 🎓"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn11 = types.KeyboardButton("США 🇺🇸")
        btn22 = types.KeyboardButton("Азия 🌏")
        btn33 = types.KeyboardButton("Канада 🇨🇦")
        back = types.KeyboardButton("Назад 🔙")
        markup.add(btn11, btn22, btn33, back)
        bot.send_message(message.chat.id, text="Выберите интересующий тебя пункт: ", reply_markup=markup)

 
    elif(message.text == "США 🇺🇸"):
        sti5 = 'CAACAgIAAxkBAAEFQ6dizyKemu6Jj6IQ8pWEssaAxyuWWwAC8wYAAnlc4gkvudvBi9GaQCkE'
        bot.send_sticker(message.chat.id, sti5)
        page = 1
        sqlTransaction = database.listColledjeForPage(tables = 'organization', order='name', Page=page, SkipSize=1)
        data = sqlTransaction[0][0] 
        count = sqlTransaction[2]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
        InlineKeyboardButton(text=f'Вперёд ->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))


        bot.send_message(message.from_user.id, f'<b>США 🇺🇸</b>\n'
                                    f'<b>{data[3]}</b>\n\n'
                                    f'<b>{data[1]}</b>\n\n'
                                    f'<b>Стоимость обучения:</b><i>{data[5]}</i>\n'
                                    f'<b>Максимальный грант:</b><i>{data[7]}</i>\n'
                                    f'<b>Сайт университета:</b><i>{data[2]}</i>\n'
                                    f'<b>Требуемые результаты SAT/IELTS:</b><i>{data[6]}</i>\n'
                                    f'<b>Дедлайн подачи заявок:</b><i> {data[4]}</i>',
                     parse_mode="HTML", reply_markup = markup)

    elif(message.text == "Азия 🌏"):
        sti5 = 'CAACAgIAAxkBAAEFQ6tizyMYMrHOuHGye3jC4WujtJltSgACUgcAAnlc4gmzAQ_HnzlQBykE'
        bot.send_sticker(message.chat.id, sti5)
        page = 1
        sqlTransaction = database.listColledjeForPage(tables = 'organization2', order='name', Page=page, SkipSize=1)
        data = sqlTransaction[0][0]
        count = sqlTransaction[2] 
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
        InlineKeyboardButton(text=f'Вперёд ->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))


        bot.send_message(message.from_user.id,f'Азия 🌏\n' 
                                    f'<b>{data[3]}</b>\n\n'
                                    f'<b>{data[1]}</b>\n\n'
                                    f'<b>Стоимость обучения:</b><i>{data[5]}</i>\n'
                                    f'<b>Максимальный грант:</b><i>{data[7]}</i>\n'
                                    f'<b>Сайт университета:</b><i>{data[2]}</i>\n'
                                    f'<b>Требуемые результаты SAT/IELTS:</b><i>{data[6]}</i>\n'
                                    f'<b>Дедлайн подачи заявок:</b><i> {data[4]}</i>',
                     parse_mode="HTML", reply_markup = markup)
                     
    elif(message.text == "Канада 🇨🇦"):
        sti7 = 'CAACAgIAAxkBAAEFRLJiz7xrAR57kWtkyb2Ov_PYOMHC_gACCwMAAu7EoQpHtJUaZj4kSykE'
        bot.send_sticker(message.chat.id, sti7)
        page = 1
        sqlTransaction = database.listColledjeForPage(tables = 'organization3', order='name', Page=page, SkipSize=1)
        data = sqlTransaction[0][0] 
        count = sqlTransaction[2]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
        InlineKeyboardButton(text=f'Вперёд ->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))


        bot.send_message(message.from_user.id, f'<b>Канада 🇨🇦</b>\n'
                                    f'<b>{data[3]}</b>\n\n'
                                    f'<b>{data[1]}</b>\n\n'
                                    f'<b>Стоимость обучения:</b><i>{data[5]}</i>\n'
                                    f'<b>Максимальный грант:</b><i>{data[7]}</i>\n'
                                    f'<b>Сайт университета:</b><i>{data[2]}</i>\n'
                                    f'<b>Требуемые результаты SAT/IELTS:</b><i>{data[6]}</i>\n'
                                    f'<b>Дедлайн подачи заявок:</b><i> {data[4]}</i>',
                     parse_mode="HTML", reply_markup = markup)


    elif(message.text == "Образовательные центры 🏫"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Logos 🧡")
        btn2 = types.KeyboardButton("Ask_consulting 💙")
        btn3 = types.KeyboardButton("bstudy.kg 💜")
        btn4 = types.KeyboardButton("globalcompass.official 🤍")
        back = types.KeyboardButton("Назад 🔙")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(message.chat.id, text="Адреса центров по поступлению зарубеж:", reply_markup=markup)

    elif(message.text == "Logos 🧡"):
        bot.send_message(message.chat.id, "LOGOS education center 1 филиал: https://2gis.kg/bishkek/geo/70000001052469306")
        bot.send_message(message.chat.id, "LOGOS education center 2 филиал: https://2gis.kg/bishkek/geo/70000001022979189")
    elif(message.text == "Ask_consulting 💙"):
        bot.send_message(message.chat.id, "ASK CONSULTING: https://2gis.kg/bishkek/geo/70000001044667351")
    elif(message.text == "bstudy.kg 💜"):
        bot.send_message(message.chat.id, "British Study Centre 1 филиал: https://2gis.kg/bishkek/geo/70000001059473424")
        bot.send_message(message.chat.id, "British Study Centre 2 филиал: https://2gis.kg/bishkek/geo/70000001020454803")
    elif(message.text == "globalcompass.official 🤍"):
        bot.send_message(message.chat.id, "ololo: https://2gis.kg/bishkek/geo/70000001032284718")
        
    elif (message.text == "Назад 🔙"):
        # bot.send_sticker(message.chat.id, sti3)
        sti3 = 'CAACAgIAAxkBAAEFQ6VizyIUVv-3TqRyIGF9wig08eaXJgAC_Q8AAoqi0EmT6eEEbPSFWCkE'
        bot.send_sticker(message.chat.id, sti3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Совет 🌥")
        button2 = types.KeyboardButton("Бакалавр 🎓")
        button3 = types.KeyboardButton("Образовательные центры 🏫")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)





    else:
        bot.send_message(message.chat.id, "Неправильный запрос ☹️")

# bot.polling(none_stop=True)


if __name__ == '__main__':
    bot.polling(none_stop=True)