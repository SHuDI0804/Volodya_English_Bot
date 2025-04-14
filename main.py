import telebot
import logging
import json
import random

from config  import api_token

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)
try:
    with open ("user_data.json","r",encoding="UTF-8") as file:
        user_data  = json.load(file)
except FileNotFoundError:
    user_data = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    logging.info("Команда/start")
    bot.send_message(message.chat.id,"Привет! Это твой бот!")

@bot.message_handler(commands=['learn'])
def handle_learn(message):
    try:
        user_words = user_data[str(message.chat.id)]
        #word = random.choice(list(user_words.keys()))                                                                                           
        # bot.send_message(message.chat.id,word)
        print(message.text)
        words_number = int(message.text.split()[1])
        ask_translation(message.chat.id,user_words,words_number)
    except Exception:
        bot.send_message(message.chat.id, "для команды '/learn' надо ввести колличество слово которое ты хочешь изучить напиример - '/learn 3'")


def ask_translation(chat_id,user_words,words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id,f"Напиши переваод слова '{word}'.")

        bot.register_next_step_handler_by_chat_id(chat_id,check_translation,translation,words_left)
    else:  
        bot.send_message(chat_id,"Урок закончен")           
    
        
def check_translation(message,expected_tarnslation,words_left):
    user_translation = message.text.strip().lower()
    if user_translation == expected_tarnslation.lower():
        bot.send_message(message.chat.id,"Правильно! Молодец!")
    else:
        bot.send_message(message.chat.id,f"Правильный перевод:{expected_tarnslation}")       

    words_left -= 1 
     
    ask_translation(message.chat.id,user_data[str(message.chat.id)], words_left) 

    




@bot.message_handler(commands=['addword']) # = /addword apple яблоко
def handle_addword(message):
    global user_data
    chat_id = str(message.chat.id)
    user_dict = user_data.get(chat_id, {})

    words = message.text.split()[1:]
    if len(words) == 2:
        words,translation = words[0].lower(),words[1].lower()
        user_dict[words] = translation
        user_data[chat_id] = user_dict

        with open ("user_data.json","w",encoding="UTF-8") as file :
            json.dump(user_data,file,ensure_ascii= False, indent = 4)
        bot.send_message(chat_id , f"слово'{words}'добавлено в словарь.")
    else:
        bot.send_message(chat_id , "Произошла ошибка .")
    



        
     



@bot.message_handler(func = lambda message: True)
def handle_all(message):
    if message.text.lower() == "как тебя зовут?":  
        bot.send_message(message.chat.id, "Я Володя")
    elif message.text.lower() == "как тебя зовут":  
        bot.send_message(message.chat.id, "Я Володя")
    elif message.text.lower() == "как дела?": 
        bot.send_message(message.chat.id, "Отлично")
    elif message.text.lower() == "как дела": 
        bot.send_message(message.chat.id, "Отлично")
    elif message.text.lower() == "расскажи о себе": 
          bot.send_message(message.chat.id, "Я бот для изучения английского языка")
    elif message.text.lower() == "расскажи шутку": 
          bot.send_message(message.chat.id, "......")     
    
    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Начинаем работу бота...")

    bot.polling(non_stop=True)  