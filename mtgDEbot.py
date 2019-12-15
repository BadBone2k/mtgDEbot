import sys
import asyncio
import telepot
import requests
import json
from pprint import pprint
from telepot.aio.helper import InlineUserHandler, AnswererMixin, ChatHandler
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open, per_inline_from_id
from telepot.namedtuple import *

"""
(vorher mit pip3.5 installieren: telepot, requests, beautifulsoup4)

$ python3.5 mtgDEbot.py <token>

Telegram Bot, der Magickarten von http://magiccards.info inline sucht.
Die Suche wurde auf deutsche Karten eingeschränkt.
So lange nichts eingegeben wurde, wird eine zufällige Karte angezeigt.

Verwendung des Bots inline: @mtgDEbot <Kartenname> [.,/| <Edition>]

Die Angabe der Edition ist optional, es gibt verschiedene Trenner,
hinter dem Trenner kann ein Leerzeichen sein, muss aber nicht.

Der ganze Code basiert auf Codebeispielen und Tutorials, die hier zu finden sind:
    https://github.com/nickoala/telepot

Danke!
"""

"""
Wird der Bot direkt angesprochen, antwortet er mit einer kleinen Anleitung.
Bisher keine expliziten Befehle wie /help oder so
"""


class ChatBot(ChatHandler):
    def __init__(self, *args, **kwargs):
        super(ChatBot, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # print(content_type, chat_type, chat_id)

        if content_type == 'text':
            # answer = msg['text']
            answer = ("Hier gibt es nicht viel zu erreichen, verwende den Bot in einem anderem (Gruppen-)Chat: " +
                      "\"@mtgDEbot Kartenname / Edition\". " +
                      "Als Trenner dürfen . , / | verwendet werden.")
            # print(answer)
            await self.sender.sendMessage(answer)


"""
Hier handelt der Bot inline in Chats und erfüllt seine eigentliche Aufgabe
"""


class InlineHandler(InlineUserHandler, AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        def compute_answer():
            api_url = 'https://api.scryfall.com/cards'
            api_search = api_url + '/search'
            api_random = api_url + '/random'
            search_lang = '?include_multilingual=true'

            trenner = tuple(["|", "/", ".", ","])
            api_call = []
            search_string = []
            edition_string = ''
            nextisedition = False
            articles = []
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

            """
            Suchbegriff in Einzelteile zerlegen und hinten die Edition extrahieren
            """
            words = query_string.split()
            for word in words:
                if word.startswith(trenner) and len(word) >= 3:
                    edition_string = word[1:]
                    break
                elif word.startswith(trenner) and len(word) == 1:
                    nextisedition = True
                elif nextisedition:
                    edition_string = word
                    break
                else:
                    search_string.append(word)

            """
            Suchstring erzeugen, falls noch nicht eingegeben wurde, wird eine zufällige Karte ausgegeben
            """
            api_call = api_url + search_lang + "+".join(search_string)
            if edition_string:
                # print(edition_string)
                edition_string = "+edition%3A" + edition_string
                api_call += edition_string

            if not query_string:
                api_call = api_random
            print(api_call)

            response = requests.get(api_call)

            """
            Bilder extrahieren
            """
            cards = json.loads(response.text)
            if cards['object'] == 'list':
                for card in cards['data']:
                    curr_img = InlineQueryResultPhoto(
                        id=card['id'],
                        photo_url=card['image_uris']['normal'],
                        thumb_url=card['image_uris']['small'],
                        photo_width=100, photo_height=140
                    )

                    print(curr_img)
                    articles.append(curr_img)

            # articles = [{'type': 'article', 'id': 'abc', 'title': query_string, 'message_text': query_string}]
            return articles

        self.answerer.answer(msg, compute_answer)

    """
    Nach Auswahl einer Karte wird hier das Ergebnis verschickt
    """

    def on_chosen_inline_result(self, msg):
        pprint(msg)
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)


"""
Die eigentliche ausführung des Bots
"""
TOKEN = sys.argv[1]  # get token from command-line
bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, ChatBot, timeout=10),
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=10),
])
loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')
loop.run_forever()
