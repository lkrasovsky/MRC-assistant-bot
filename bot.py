import telebot

import constants
import utils

bot = telebot.TeleBot(constants.token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    id: str = str(message.from_user.id)
    bot.send_message(id, "Привет. Введи номер своей группы.",
                     reply_markup=utils.create_groups_keyboard())


@bot.message_handler(content_types=['text'])
def message_handler(message):
    id: str = str(message.from_user.id)
    if "к" in message.text or "6" in message.text:
        if utils.set_users_page(id, message.text):

            bot.send_message(id, "Принято.",
                             reply_markup=utils.create_menu_keyboard())
        else:
            bot.send_message(id, "Перезапустите бота.")


    elif message.text == "Расписание 📋":
        try:
            utils.get_schedule()
            page = utils.get_page(message)

            if page != 0:
                with open("rasp/" + "page_" + page + ".jpg", 'rb') as photo:
                    bot.send_chat_action(id, 'upload_photo')
                    bot.send_photo(id, photo)
            else:
                bot.send_message(id, "Введите номер группы снова.", reply_markup=utils.create_groups_keyboard())

        except TypeError:
            bot.send_message(id, "В данный момент расписание недоступно((")

    elif message.text == "Номера преподов ☎":
        bot.send_message(id, "Этот раздел находится на стадии разработки.")
    elif message.text == "Сайт 🌎":
        bot.send_message(id, "http://www.mrk-bsuir.by/ru")
    elif message.text == "Изменить группу":
        bot.send_message(id, "Выберите группу.", reply_markup=utils.create_groups_keyboard())
    elif message.text == "О боте ❔":
        bot.send_message(id, "Этот раздел находится на стадии разработки.")
    elif message.text == "Автор 🙇🏼":
        bot.send_message(id, "Лев Красовский\n@lkrasovsky\n\nгр. 8к1391")


bot.polling(none_stop=True, interval=0)
