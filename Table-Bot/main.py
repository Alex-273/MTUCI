import telebot, psycopg2
from telebot import types
import datetime

token = "2119188135:AAFDWjBa27_akUwTv89pksJ2wIBXSjDRRV0"
bot = telebot.TeleBot(token)

day = datetime.date(2021, 8, 30)
day = str(day).split('-')

conn = psycopg2.connect(database="week_db",
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()
cursor2 = conn.cursor()
cursor3 = conn.cursor()

rowNu = [0] * 1000


def mass(day):
    cursor3.execute("SELECT id FROM week.{} order by id;".format(day))
    records2 = list(cursor3.fetchall())
    for y, u in enumerate(records2):
        rowNu[y] = u[0]


def check_day(s):
    if s == "понедельник":
        mass("monday")
        return "monday"
    elif s == "вторник":
        mass("tuesday")
        return "tuesday"
    elif s == "среда":
        mass("wednesday")
        return "wednesday"
    elif s == "четверг":
        mass("thursday")
        return "thursday"
    elif s == "пятница":
        mass("friday")
        return "friday"


def week():
    difTime = datetime.date(int(day[0]), int(day[1]), int(day[2]))
    bb = datetime.date.today()
    cc = bb - difTime
    dd = str(cc)
    num = ((int(dd.split()[0]) // 7 + 1) % 2)
    if num == 0:
        num = 2
    return num


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "вторник", "Среда", "Четверг", "Пятница")
    keyboard.row("Расписание на текущую неделю", "Расписание на след неделю")
    bot.send_message(message.chat.id, 'Я вас слушаю...', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Бот - расписание:' + "\r\n"
                                                            'Напишите команду /start для старта')


@bot.message_handler(commands=['week'])
def start_message(message):
    num = week()
    if num == 1:
        bot.send_message(message.chat.id, 'Верхняя')
    else:
        bot.send_message(message.chat.id, 'Нижняя')


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'Тогда вам сюда - https://mtuci.ru/')


@bot.message_handler(content_types=['text'])
def answer(message):
    if (message.text.lower() == "понедельник") | (message.text.lower() == "вторник") | (
            message.text.lower() == "среда") | (message.text.lower() == "четверг") | (
            message.text.lower() == "пятница") | (message.text.lower() == "расписание на текущую неделю") | (
            message.text.lower() == "расписание на след неделю"):
        if (message.text.lower() == "понедельник") | (message.text.lower() == "вторник") | (
                message.text.lower() == "среда") | (message.text.lower() == "четверг") | (
                message.text.lower() == "пятница"):
            s = ""
            i = 0
            num = week()
            now = check_day(message.text.lower())
            cursor.execute("SELECT COUNT(*) FROM week.{}".format(now))
            q = str(message.text.lower()) + ":"
            p = cursor.fetchone()[0]
            if int(p) != 0:
                for k in range(0, int(p)):
                    cursor.execute("SELECT * FROM week.{} WHERE id={}".format(now, rowNu[k]))
                    cursor2.execute("SELECT day FROM week.{} WHERE id={}".format(now, rowNu[k]))
                    records = list(cursor.fetchall())
                    o = cursor2.fetchone()[0]
                    if (str(o) == '0') | (str(o) == str(num)):
                        i = i + 1
                        s = str(s) + str(i) + "." + "  |  " + records[0][2] + "  |  " + records[0][3] + "  |  " + \
                            records[0][
                                4] + "  |  " + records[0][5] + "\r\n" + "\r\n"
            bot.send_message(message.chat.id, q + "\r\n" +
                             "------------------------------" + "\r\n" + "\r\n" +
                             s +
                             "------------------------------"
                             )
        elif (message.text.lower() == "расписание на текущую неделю") | (
                message.text.lower() == "расписание на след неделю"):
            if message.text.lower() == "расписание на текущую неделю":
                num = week()
            else:
                if week() == 1:
                    num = 2
                else:
                    num = 1
            list_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
            for e in list_days:
                i = 0
                s = ""
                cursor.execute("SELECT COUNT(*) FROM week.{}".format(e))
                q = str(e)
                mass(str(e))
                p = cursor.fetchone()[0]
                if int(p) != 0:
                    for k in range(0, int(p)):
                        cursor.execute("SELECT * FROM week.{} WHERE id={}".format(e, rowNu[k]))
                        cursor2.execute("SELECT day FROM week.{} WHERE id={}".format(e, rowNu[k]))
                        records = list(cursor.fetchall())
                        o = cursor2.fetchone()[0]
                        if (str(o) == '0') | (str(o) == str(num)):
                            i = i + 1
                            s = str(s) + str(i) + "." + "  |  " + records[0][2] + "  |  " + records[0][3] + "  |  " + \
                                records[0][
                                    4] + "  |  " + records[0][5] + "\r\n" + "\r\n"
                bot.send_message(message.chat.id, q + "\r\n" +
                                 "------------------------------" + "\r\n" + "\r\n" +
                                 s +
                                 "------------------------------"
                                 )
    else:
        bot.send_message(message.chat.id, "Я вас не понял")


bot.polling(none_stop=True, interval=0)
