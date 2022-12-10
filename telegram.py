import telebot

bot = telebot.TeleBot(token = '5967901795:AAFZhs7_fsXqf4Qt6DvzHp9F1vLqPkhXk-M')
owner_id = 542387853

homework = ""
question_list = []
class Question:
    def __init__(self,message, question_text, autor):
        self.message = message
        self.question_text = question_text
        self.autor = autor
@bot.message_handler(commands=["setdz"])
def setdz(message):
    global homework
    if message.chat.id == owner_id:
        homework = message.text.split(' ', maxsplit = 1)[1]
        bot.reply_to(message, "Домашнее задание установлено.")

@bot.message_handler(commands=["dz"])
def dz(message):
    global homework
    bot.reply_to(message,homework)

@bot.message_handler(commands=["question"])
def question(message):
    try:
        question_text = message.text.split(' ', maxsplit = 1)[1]
        bot.reply_to(message,"Вопрос отправлен, ожидайте ответа...")
        question_list.append(Question(message, question_text, message.from_user.username))
        bot.send_message(owner_id,f"У вас новый вопрос всего {len(question_list)} вопросов")
    except:
        bot.reply_to(message,"Введите вопрос")
@bot.message_handler(commands=['quest'])
def show_quest(message):
    if message.chat.id == owner_id:
        j = 1
        for i in question_list:
            bot.send_message(owner_id, f'{j}: {i.question_text} (от @{i.autor})')
            j += 1
@bot.message_handler(commands=['answer'])
def answer(message):
    global question_list
    text = message.text.split(' ', maxsplit = 2)[2]
    id = message.text.split(' ', maxsplit = 2)[1]
    question = question_list[int(id) - 1]
    bot.reply_to(question.message, text)
    del question_list[int(id)- 1]
    bot.reply_to(message, 'Ответ отправлен')

bot.infinity_polling()