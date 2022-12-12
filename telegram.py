import telebot
from gtts import gTTS
import os
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
    try:
        if message.chat.id == owner_id:
            homework = message.text.split(' ', maxsplit = 1)[1]
            bot.reply_to(message, "Домашнее задание установлено.")
    except:
        pass

@bot.message_handler(commands=["dz"])
def dz(message):
    global homework
    try:
        bot.reply_to(message,homework)
    except:
        pass

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
    try:
        if message.chat.id == owner_id:
            j = 1
            for i in question_list:
                bot.send_message(owner_id, f'{j}: {i.question_text} (от @{i.autor})')
                j += 1
    except:
        pass
@bot.message_handler(commands=['answer'])
def answer(message):
    global question_list
    try:
        text = message.text.split(' ', maxsplit = 2)[2]
        id = message.text.split(' ', maxsplit = 2)[1]
        question = question_list[int(id) - 1]
        bot.reply_to(question.message, text)
        del question_list[int(id)- 1]
        bot.reply_to(message, 'Ответ отправлен')
    except:
        pass
PATH = os.path.abspath(__file__ + "/..")

@bot.message_handler(commands = ['voice'])
def text_to_audio(message):
    try:
        text = message.text.split(' ',maxsplit=1)[1]
        audio = gTTS(text=text, lang=message.from_user.language_code, slow=False)
        audio.save(PATH + "/audio.mp3")
        audio = open(PATH + "/audio.mp3", 'rb')
        bot.send_voice(message.chat.id, audio)
    except:
        pass

@bot.message_handler(content_types = ['new_chat_members'])
def new_member(message):
    try:
        user_name = message.from_user.username
        bot.send_message(message.chat.id, '@' + user_name + ' Кажется у нас новый ученик.')
    except:
        pass
#До встречи

bot.infinity_polling()