import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import urllib.request
import bs4 as bs

bot = telepot.Bot("BOT_TOKEN")

whitelist = set("1234567890,")

def control_text(msg):
    component_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Case', callback_data='case')],
        [InlineKeyboardButton(text='Processore', callback_data='processore')],
        [InlineKeyboardButton(text='Scheda madre', callback_data='scheda madre')],
        [InlineKeyboardButton(text='Dissipatore', callback_data='dissipatore')],
        [InlineKeyboardButton(text='RAM', callback_data='ram')],
        [InlineKeyboardButton(text='SSD', callback_data='ssd')],
        [InlineKeyboardButton(text='Hard disk', callback_data='hard disk')],
        [InlineKeyboardButton(text='Alimentatore', callback_data='alimentatore')],
        [InlineKeyboardButton(text='Tastiera', callback_data='tastiera')],
        [InlineKeyboardButton(text='Mouse', callback_data='mouse')],
        [InlineKeyboardButton(text='Monitor', callback_data='monitor')],
        [InlineKeyboardButton(text='Casse', callback_data='casse')],
        ])
    content_type, chat_type, chat_id = telepot.glance(msg)
	
    if content_type == "text":
        txt = msg['text']
        if txt == "/start":
            first_name = msg["chat"]["first_name"]
            bot.sendMessage(chat_id, "Benvenuto " + first_name + ", ti trovi sul bot.")
            bot.sendMessage(chat_id, "Di quale componente vuoi controllare il prezzo?",  reply_markup=component_keyboard)

def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    if query_data == "case":
        try:
            sauce = urllib.request.urlopen("https://www.amazon.it/Corsair-SPEC-OMEGA-Gaming-Mid-Tower-Temperato/dp/B07B2YJXLM/ref=sr_1_1?ie=UTF8&qid=1545163655&sr=8-1&keywords=case+corsair+rgb").read()
            soup = bs.BeautifulSoup(sauce, "html.parser")

            for item in soup.find_all("span", "a-size-medium a-color-price"):
                answer = "".join(filter(whitelist.__contains__, item.text))

                if ",00" in answer:
                    conta = 0
                    for lettera in answer:
                        conta = conta + 1
                    if conta == 6:
                        answer = answer[:3] + "€"
                    else:
                        answer = answer[:2] + "€"

        except urllib.error.HTTPError as err:
            if err.code == 404:
                bot.sendMessage(chat_id, "Errore, prezzo non trovato")

        bot.sendMessage(chat_id, answer)

MessageLoop(bot, {'chat': control_text,
                  'callback_query': on_callback_query}).run_as_thread()


            #soup = bs4.BeautifulSoup(sorgente)
    #elenco = soup.findAll('span id')
    #if elenco:
            #for a in elenco:
            #print(a)











