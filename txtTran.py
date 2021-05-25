from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot


def text_translate(text, lanuage):

    from ibm_watson import LanguageTranslatorV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    url_lt = '.'
    apikey_lt = '.'
    version_lt = '2018-05-01'
    authenticator = IAMAuthenticator(apikey_lt)
    language_translator = LanguageTranslatorV3(
        version=version_lt, authenticator=authenticator)
    language_translator.set_service_url(url_lt)

    from pandas import json_normalize

    json_normalize(
        language_translator.list_identifiable_languages().get_result(), "languages")
    translation_response = language_translator.translate(
        text=text, model_id=lanuage)

    translation = translation_response.get_result()

    spanish_translation = translation['translations'][0]['translation']
    return(spanish_translation)

# bot 

API_TOKEN = '.'


bot = telebot.TeleBot(API_TOKEN)
selectedLanguage = {}


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("EN to AR", callback_data="en-ar"),
               InlineKeyboardButton("AR to EN", callback_data="ar-en"))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the translation bot")
    msg = bot.send_message(
        message.chat.id, "Choose the language ?", reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "en-ar":
            selectedLanguage['language'] = 'en-ar'
            bot.send_message(call.from_user.id, 'ارسل رسالتك الان')

        elif call.data == "ar-en":
            selectedLanguage['language'] = 'ar-en'
            bot.send_message(call.from_user.id, "Send your message")
    except:
        bot.send_message(call.from_user.id,'something went wrong try agin later')


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    try:
        bot.send_message(message.chat.id, text_translate(
            message.text, selectedLanguage['language']))
    except:
        bot.send_message(message.chat.id,'something went wrong try agin later')



bot.polling()
