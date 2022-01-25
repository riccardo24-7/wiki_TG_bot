
import telebot
import wikipedia
import re
from config.myconfig import TOKEN_BOT


bot = telebot.TeleBot(TOKEN_BOT)

@bot.message_handler(commands=["start", "help"])
def start_bot(message):
    cid = message.chat.id
    text = message.text
    if text == "/start":
        bot.send_message(cid, "/enwiki - English wikipedia\n/ruwiki - Русская википедия")
    elif text == "/help":
        pass
    
    
@bot.message_handler(commands=["enwiki", "ruwiki"])
def wiki_language(message):
    cid = message.chat.id
    text = message.text
    if text == "/enwiki":
        wikipedia.set_lang("en")
        msg = bot.send_message(cid, "Enter any word to search Wikipedia")
        bot.register_next_step_handler(msg, enwiki_search)
    elif text == "/ruwiki":
        wikipedia.set_lang("ru")
        msg = bot.send_message(cid, "Введите любое слово для поиска в Wikipedia") 
        bot.register_next_step_handler(msg, ruwiki_search)

       
def enwiki_search(message):
    cid = message.chat.id
    text = message.text
    try:
        wiki_res = wikipedia.page(text).content[:1000]
        wiki_sentences = wiki_res.split(".")[:-1]
        wiki_result = ""
        for sentence in wiki_sentences:
            if not("==" in sentence):
                if len(sentence.strip()) > 3:
                    wiki_result += sentence + "."
            else:
                break
        wiki_result = re.sub(r"\([^()]*\)", "", wiki_result)
        wiki_result = re.sub(r"\{[^\{\}]*\}", "", wiki_result)
        bot.send_message(cid, wiki_result, parse_mode="HTML")
    except Exception as e:
        print(e)
        bot.send_message(cid, "We can't find this")

def ruwiki_search(message):
    cid = message.chat.id
    text = message.text
    try:
        wiki_res = wikipedia.page(text).content[:1000]
        wiki_sentences = wiki_res.split(".")[:-1]
        wiki_result = ""
        for sentence in wiki_sentences:
            if not("==" in sentence):
                if len(sentence.strip()) > 3:
                    wiki_result += sentence + "."
            else:
                break
        wiki_result = re.sub(r"\([^()]*\)", "", wiki_result)
        wiki_result = re.sub(r"\{[^\{\}]*\}", "", wiki_result)
        bot.send_message(cid, wiki_result, parse_mode="HTML")
    except Exception as e:
        print(e)
        bot.send_message(cid, "Не могу найти этот запрос")       
        
        
        

bot.polling(none_stop=True, interval=0)