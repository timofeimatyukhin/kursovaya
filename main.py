import telebot
from telebot import types
import webbrowser
import os

bot = telebot.TeleBot('6776079456:AAHjPEbBYIAhyOgLNounK9zQMSTHaWXSyho')
login = '123'
password = '123'
wastes = list() ##список трат
purpose = 0## цель
fillpur = 0## прогресс выполнения цели
prflag = 0 ## флаг создания цели
frflag = 0 ## флаг заморозки
regflag = 0 ## флаг регистрации
regerr = 0 ## флаг ошибки ввода логина/пароля
bank = 0 ## общий счет
convert = 0 ## конверт
isboxcreated = 0 ## флаг на создание конверта
inoutflag = 0 ## флаг на ввод/вывод средств с общего счета
inoutflagcon = 0 ## флаг на ввод/вывод средств с конверта
in_error = 0 ## флаг на ошибку ввода в конверте

##начало работы
@bot.message_handler(commands = ['start'])
def start(message):
    global regerr
    if regerr == 0 and regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Привет, я ваш финансовый ассистент.\n'
                                          'Для начала работы нужно авторизироваться.\n', reply_markup=markup)
    elif regerr == 1 and regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Попробуйте еще раз', reply_markup=markup)
        regerr = 0
    elif regerr == 0 and regflag == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
        bot.send_message(message.chat.id, 'Вы уже авторизировались.', reply_markup=markup)



@bot.message_handler(commands = ['exit'])
def exit(message):
    global regflag
    if regflag == 1:
        regflag = 0
        bot.send_message(message.chat.id, 'Вы успешно вышли с профиля.')
        start(message)
    elif regflag == 0:
        bot.send_message(message.chat.id, 'Вы еще не авторизировались.')
        start(message)


@bot.message_handler(commands = ['freezing'])
def freezing(message):
    global frflag
    if regflag == 1:
        if frflag == 0:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, '❄️Ваш основной счет заморожен.', reply_markup=markup)
            frflag = 1
        elif frflag == 1:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, '❄️Ваш основной счет разморожен.', reply_markup=markup)
            frflag = 0
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)


@bot.message_handler(commands = ['createpurpose'])
def precreate(message):
    if regflag == 1:
        if prflag == 0:
            bot.send_message(message.chat.id, 'На какую сумму вы хотите создать цель?')
            bot.register_next_step_handler(message, create)
        elif prflag == 1:
            markup = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton('К цели', callback_data='showpurpose')
            btn2 = telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu')
            markup.row(btn1,btn2)
            bot.send_message(message.chat.id, 'Цель уже создана.', reply_markup=markup)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)


def create(message):
    global purpose
    global prflag
    mess = message.text
    if mess.isdigit() == True:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
        bot.send_message(message.chat.id, '✏️Цель успешно создана.', reply_markup=markup)
        purpose = int(mess)
        prflag = 1
    elif mess.isdigit() == False and mess[0] == '-':
        bot.send_message(message.chat.id, 'Нельзя создать цель на отрицательную сумму!')
        precreate(message)
    elif mess.isdigit() == False:
        bot.send_message(message.chat.id, 'Ввод производится исключительно в формате целого числа!')
        precreate(message)


@bot.message_handler(commands=['showpurpose'])
def showpurpose(message):
    if regflag == 1:
        if prflag == 1:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, f'📊Данные по вашей цели:\n'
                                              'Выполнено:' + str(fillpur) + '/' + str(purpose) + 'р', reply_markup=markup)
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, 'Цель еще не создана.',
                             reply_markup=markup)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)


@bot.message_handler(commands=['editpurpose'])
def preeditpurpose(message):
    if regflag == 1:
        if prflag == 1:
            bot.send_message(message.chat.id, '📎Ваша цель: ' + str(purpose) + 'р\n'
                                                                             'Введите число, на которое хотите редактировать вашу цель:')
            bot.register_next_step_handler(message, editpurpose)
        elif prflag == 0:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Создать цель', callback_data='createpurpose'))
            bot.send_message(message.chat.id, 'Цель еще не создана.', reply_markup=markup)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)


def editpurpose(message):
    global purpose
    global prflag
    mess = message.text
    if mess.isdigit() == True:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
        bot.send_message(message.chat.id, '✏️Цель успешно редактирована.', reply_markup=markup)
        purpose = int(mess)
    elif mess.isdigit() == False and mess[0] == '-':
        bot.send_message(message.chat.id, 'Нельзя редактировать цель на отрицательную сумму!')
        precreate(message)
    elif mess.isdigit() == False:
        bot.send_message(message.chat.id, 'Ввод производится исключительно в формате целого числа!')
        precreate(message)


@bot.message_handler(commands=['deletepurpose'])
def delete(message):
    global prflag
    if regflag == 1:
        if prflag == 1:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, '✏️Цель успешно удалена.', reply_markup=markup)
            prflag = 0
        elif prflag == 0:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, 'Цель еще не создана.', reply_markup=markup)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)


@bot.message_handler(commands=['checkwastes'])
def check(message):
    global wastes
    if regflag == 1:
        summ = 0
        printing = '💳Анализ расходов:\n'
        for i in range (0, len(wastes)):
            if i != len(wastes) - 1:
                printing += str(wastes[i]) + 'р' + ', '
            elif i == len(wastes) - 1:
                printing += str(wastes[i]) + 'р'
            summ += wastes[i]
        printing += '\n Общая сумма расходов: ' + str(summ) + 'р'
        if len(wastes) > 0:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, '' + printing, reply_markup=markup)
        elif len(wastes) == 0:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
            bot.send_message(message.chat.id, 'Расходов пока что не было.', reply_markup=markup)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)

@bot.message_handler(commands = ['work'])
def work(message):
    if regflag == 1:
        bot.send_message(message.chat.id, '👍🏻Приступим! Что бы вы хотели сделать?\n'
                                          '✅/inoutmoney - Внесениe/вывод средств с основного счета\n'
                                          '✅/checkwastes - Анализ расходов\n'
                                          '✅/createbox - Создать конверт\n'
                                          '✅/inputcon - Внести средства на конверт\n'
                                          '✅/outputcon - Вывести средства с конверта\n'
                                          '✅/showbalance - Показать баланс на основном счете\n'
                                          '✅/showallbalance - Показать баланс на основном счете и в конверте\n'
                                          '✅/freezing - Заморозить/разморозить основной счет\n'
                                          '✅/createpurpose - Создать цель\n'
                                          '✅/editpurpose - Редактировать цель\n'
                                          '✅/showpurpose - Показать цель\n'
                                          '✅/deletepurpose - Удалить цель\n'
                                          '✅/exit - Выйти с профиля\n'
                                          '✅/clean - Выполнить полный сброс')
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)



##вывод информации о боте
@bot.message_handler(commands = ['info'])
def info(message):
    bot.send_message(message.chat.id, '\U00002753Для чего же нужен этот бот?\n1️⃣Во-первых, он поможет вам внести и снять деньги с вашего личного виртуального счета\n'
                         '2️⃣Во-вторых, с ним вы сможете удобно и быстро проанализировать ваши расходы\n'
                         '3️⃣В-третьих, вы сможете легко завести отдельный конверт с целью накопления на мечту\n'
                         '4️⃣В-четвертых, в одно касание вы сможете узнать ваш настоящий баланс\n'
                         '5️⃣В-пятых, вы легко сможете заморозить/разморозить ваш счет для его полной безопасности\n'
                         '6️⃣Ну и наконец, вы сможете поставить себе цель заработка на следующий месяц\n'
                         '\U00002714И все это только с нашим ботом')


##ввод-вывод денег
@bot.message_handler(commands = ['inoutmoney'])
def inoutmoney(message):
    if regflag == 1 and frflag == 0:
        bot.send_message(message.chat.id, '📌Выберите действие:\n📌/input - Внести деньги\n📌/output - Вывести деньги')
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)
    elif regflag == 1 and frflag == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
        bot.send_message(message.chat.id, '❄️Ваш основной счет заморожен. Внесение и снятие средств недоступны.', reply_markup=markup)

##внесение денег
@bot.message_handler(commands = ['input'])
def input(message):
    global inoutflag
    if regflag == 1 and frflag == 0:
        inoutflag = 1
        bot.send_message(message.chat.id, '📌Сколько денег вы хотите внести?')
        bot.register_next_step_handler(message, show_balance)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)
    elif regflag == 1 and frflag == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
        bot.send_message(message.chat.id, '❄️Ваш основной счет заморожен. Внесение и снятие средств недоступны.',
                         reply_markup=markup)
##снятие денег
@bot.message_handler(commands = ['output'])
def output(message):
    global inoutflag
    if regflag == 1 and frflag == 0:
        inoutflag = 0
        bot.send_message(message.chat.id, '📌Сколько денег вы хотите снять?\n Доступно к списанию: %d р' % bank)
        bot.register_next_step_handler(message, show_balance)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)
    elif regflag == 1 and frflag == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
        bot.send_message(message.chat.id, '❄️Ваш основной счет заморожен. Внесение и снятие средств недоступны.',
                         reply_markup=markup) 


@bot.message_handler(commands = ['createbox'])
def createbox(message):
    global isboxcreated
    global in_error
    if regflag == 1:
        if isboxcreated == 0:
            bot.send_message(message.chat.id, '✉️Конверт успешно создан.\n/inputcon - пополнить конверт\n/outputcon - снять средства с конверта')
            isboxcreated = 1
        elif isboxcreated == 1 and in_error == 0:
            bot.send_message(message.chat.id, '✉️Конверт уже создан.\n/inputcon - пополнить конверт\n/outputcon - снять средства с конверта')
        elif isboxcreated == 1 and in_error == 1:
            bot.send_message(message.chat.id, '✉️Попробуйте еще раз.\n/inputcon - пополнить конверт\n/outputcon - снять средства с конверта')
            in_error = 0
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)



@bot.message_handler(commands = ['inputcon'])
def inputcon(message):
    global inoutflagcon
    if regflag == 1:
        inoutflagcon = 1
        bot.send_message(message.chat.id, '✉️Сколько денег вы хотите положить в конверт?')
        bot.register_next_step_handler(message, convert_work)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)


@bot.message_handler(commands = ['outputcon'])
def outputcon(message):
    global inoutflagcon
    if regflag == 1:
        inoutflagcon = 0
        bot.send_message(message.chat.id, '✉️Сколько денег вы хотите снять?\nДоступно к списанию с конверта: %d р' % convert)
        bot.register_next_step_handler(message, convert_work)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)




def convert_work(message):
    global convert
    global in_error
    global isboxcreated
    if isboxcreated == 1:
        mess = message.text
        if mess.isdigit() == True:
            if int(mess) >= 0:
                oldconv = convert
                if inoutflagcon == 1:
                    convert += int(mess)
                elif inoutflagcon == 0 and convert > int(mess):
                    convert -= int(mess)
                elif inoutflagcon == 0 and convert < int(mess):
                    in_error = 1
                    bot.send_message(message.chat.id, '❗Запрашиваемая сумма больше вашего баланса в конверте')

                    createbox(message)

                if oldconv < convert:
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton('Показать баланс', callback_data='balancecon'))
                    bot.send_message(message.chat.id, '📌Деньги успешно внесены в конверт!', reply_markup=markup)

                elif oldconv == convert and int(mess) == 0:
                    in_error = 1
                    bot.send_message(message.chat.id, '❗Я не могу внести 0 рублей❗')

                    createbox(message)

                elif oldconv > convert:
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton('Показать баланс', callback_data='balancecon'))
                    bot.send_message(message.chat.id, '📌Деньги успешно сняты со с конверта!', reply_markup=markup)

        elif mess.isdigit() != True and mess[0] != '-':
            in_error = 1
            bot.send_message(message.chat.id, '❗Вписывать сумму нужно исключительно в формате целого числа❗')

            createbox(message)

        elif int(mess) < 0 and mess[0] == '-':
            in_error = 1
            bot.send_message(message.chat.id, '❗Вы ввели отрицательную сумму❗')

            createbox(message)
    elif isboxcreated == 0:
        bot.send_message(message.chat.id, '❗Конверт еще не создан❗\n /createbox - создать конверт')



##показать баланс
def show_balance(message):
    global bank
    global wastes
    global fillpur
    global purpose
    mess = message.text
    if mess.isdigit() == True:
        if int(mess) >= 0:
            oldbank = bank
            if inoutflag == 1:
                bank += int(mess)
                if prflag == 1:
                    fillpur += bank - oldbank
            elif inoutflag == 0 and bank > int(mess):
                bank -= int(mess)
                wastes.append(int(mess))
            elif inoutflag == 0 and bank < int(mess):
                bot.send_message(message.chat.id, '❗Запрашиваемая сумма больше вашего баланса❗')
                inoutmoney(message)

            if oldbank < bank and (fillpur < purpose or purpose == 0):
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('Показать баланс', callback_data='balance'))
                bot.send_message(message.chat.id, '📌Деньги успешно внесены на счет!', reply_markup=markup)
            elif oldbank < bank and fillpur >= purpose and purpose != 0:
                markup = telebot.types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Показать баланс', callback_data='balance')
                btn2 = types.InlineKeyboardButton('К цели', callback_data='showpurpose')
                markup.row(btn1,btn2)
                bot.send_message(message.chat.id, '📌Деньги успешно внесены на счет! \n'
                                                  '🎉А также выполнена цель. Поздравляем!', reply_markup=markup)





            elif oldbank == bank and int(mess) == 0:
                bot.send_message(message.chat.id, '❗Я не могу внести 0 рублей❗')
                inoutmoney(message)

            elif oldbank > bank:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton('Показать баланс', callback_data='balance'))
                bot.send_message(message.chat.id, '📌Деньги успешно сняты со счета!', reply_markup=markup)

    elif mess.isdigit() != True and mess[0] != '-':
        bot.send_message(message.chat.id, '❗Вписывать сумму нужно исключительно в формате целого числа❗')
        inoutmoney(message)

    elif int(mess) < 0 and mess[0] == '-':
        bot.send_message(message.chat.id, '❗Вы ввели отрицательную сумму❗')
        inoutmoney(message)

@bot.message_handler(commands = ['showbalance']) ##показать баланс отдельная кнопка
def balance(message):
    if regflag == 1:
        bot.send_message(message.chat.id, 'Ваш баланс на основном счете: %d р' % bank)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)
        
@bot.message_handler(commands = ['showallbalance'])
def allbalance(message):
    if regflag == 1:
        bot.send_message(message.chat.id, 'Ваш баланс на основном счете: %d р' % bank)
        bot.send_message(message.chat.id, 'Ваш баланс на конверте: %d р' % convert)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)





## установка логина
def reg_login(message):
    global login
    if message.text[0] != '/':
        if message.text == login:
            bot.send_message(message.chat.id, 'Отлично! Теперь введите пароль:')
            bot.register_next_step_handler(message, reg_password)
        elif message.text != login:
            bot.send_message(message.chat.id, 'Логин введен неверно! Попробуйте еще раз.')
            start(message)

    else:
        global regerr
        regerr = 1
        bot.send_message(message.chat.id, 'Логин не может начинаться со знака /.')
        start(message)


## установка пароля
def reg_password(message):
    global password
    if message.text[0] != '/':
        if message.text == password:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Начать', callback_data='enter'))
            bot.send_message(message.chat.id, 'Готово, теперь мы можем начать работу.', reply_markup=markup)
        elif message.text != password:
            bot.send_message(message.chat.id, 'Пароль введен неверно! Попробуйте еще раз.')
            start(message)
    else:
        global regerr
        regerr = 1
        bot.send_message(message.chat.id, 'Пароль не может начинаться со знака /.')
        start(message)




##вывод баланса
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global wastes
    global purpose
    global fillpur
    global prflag
    global frflag
    global regflag
    global regerr
    global bank
    global convert
    global isboxcreated
    global inoutflag
    global inoutflagcon
    global in_error
    if call.data == 'balance':
        bot.send_message(call.message.chat.id, 'Ваш баланс на основном счете: %d р' % bank)
    elif call.data == 'balancecon':
        bot.send_message(call.message.chat.id, 'Ваш баланс на конверте: %d р' % convert)
    elif call.data == 'register':
        global login
        bot.send_message(call.message.chat.id, 'Введите логин:')
        bot.register_next_step_handler(call.message, reg_login)
    elif call.data == 'enter':
        bot.send_message(call.message.chat.id, '🎉Отлично, вы авторизировались! Чем могу быть полезен?\n'
                                          '/info - все о боте\n'
                                          '/work - начать работу')
        regflag = 1
    elif call.data == 'mainmenu':
        work(call.message)
    elif call.data == 'showpurpose':
        showpurpose(call.message)
    elif call.data == 'createpurpose':
        precreate(call.message)
    elif call.data == 'clean':
        wastes = list()  ##список трат
        purpose = 0  ## цель
        fillpur = 0  ## прогресс выполнения цели
        prflag = 0  ## флаг создания цели
        frflag = 0  ## флаг заморозки
        regflag = 0  ## флаг регистрации
        regerr = 0  ## флаг ошибки ввода логина/пароля
        bank = 0  ## общий счет
        convert = 0  ## конверт
        isboxcreated = 0  ## флаг на создание конверта
        inoutflag = 0  ## флаг на ввод/вывод средств с общего счета
        inoutflagcon = 0  ## флаг на ввод/вывод средств с конверта
        in_error = 0  ## флаг на ошибку ввода в конверте
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu'))
        bot.send_message(call.message.chat.id, 'Сброс выполнен успешно.', reply_markup=markup)

@bot.message_handler(commands=['clean'])
def clean(message):
    global wastes, purpose, fillpur, prflag, frflag, regflag, regerr, bank, convert, isboxcreated, inoutflag, inoutflagcon, in_error
    if regflag == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('Выполнить сброс', callback_data='clean')
        btn2 = telebot.types.InlineKeyboardButton('Вернуться', callback_data='mainmenu')
        markup.row(btn1,btn2)
        bot.send_message(message.chat.id, 'Вы уверены? Восстановить данные после сброса будет невозможно.', reply_markup=markup)
    elif regflag == 0:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Войти', callback_data='register'))
        bot.send_message(message.chat.id, 'Для начала работы необходимо авторизироваться!', reply_markup=markup)

bot.polling(non_stop=True)