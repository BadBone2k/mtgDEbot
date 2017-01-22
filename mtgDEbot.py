import sys
import asyncio
import telepot
import requests
from pprint import pprint
from telepot.aio.helper import InlineUserHandler, AnswererMixin, ChatHandler
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open, per_inline_from_id
from bs4 import BeautifulSoup as bs

"""
(vorher mit pip3.5 installieren: telepot, requests, beautifulsoup4)

$ python3.5 mtgDEbot.py <token>

Telegram Bot, der Magickarten von http://magiccards.info inline sucht.
Die Suche wurde auf deutsche Karten eingeschränkt.
So lange nicht eingegeben wurde, wird eine zufällige Karte angezeigt.
"""

class MessageCounter(ChatHandler):
	def __init__(self, *args, **kwargs):
		super(MessageCounter, self).__init__(*args, **kwargs)
		self._count = 0

	async def on_chat_message(self, msg):
		#self._count += 1
		content_type, chat_type, chat_id = telepot.glance(msg)
		#print(content_type, chat_type, chat_id)
		
		if content_type == 'text':
			#strOut = str(self._count) + ': ' + msg['text']
			strOut = ("Hier gibt es nicht viel zu erreichen, verwende den Bot in einem anderem (Gruppen-)Chat: " +
			"\"@mtgDEbot Kartenname / Edition\". " +
			"Als Trenner dürfen . , / | verwendet werden.")
			#print(strOut)
			await self.sender.sendMessage(strOut)

class InlineHandler(InlineUserHandler, AnswererMixin):
	def __init__(self, *args, **kwargs):
		super(InlineHandler, self).__init__(*args, **kwargs)
		
	def on_inline_query(self, msg):
		def compute_answer():
			session = requests.Session()
			headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'}
			search_url = 'http://magiccards.info/query'
			trenner = tuple(["|", "/", ".", ","])
			search_string = []
			edition_string = []
			nextisedition_bool = False
			
			query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
			#print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)
			
			words = query_string.split()
			for word in words:
				if word.startswith(trenner) and len(word) >= 4:
					edition_string = word[1:4]
					break
				elif word.startswith(trenner) and len(word) == 1:
					nextisedition_bool = True
				elif nextisedition_bool:
					edition_string = word[:3]
					break
				else:
					search_string.append(word)
			
			search_string = search_url + '?q=l%3Ade+' + "+".join(search_string)
			if edition_string:
				print(edition_string)
				edition_string = "+e%3A" + edition_string + "%2Fde"
				search_string = search_string + edition_string
			search_string = search_string + '&v=scan&s=cname'
			
			if not query_string:
				search_string = 'http://magiccards.info/random.html'
			print(search_string)
			
			response = session.get(search_string, headers=headers)
			articles = []
			#print(response.text)
			
			soup = bs(response.text, "html.parser")
			for imgtag in soup.find_all('img'):
				if int(imgtag['width']) > 50:
					#print(imgtag['src'])
					curr_img = {
					"type": "photo",
					"id": imgtag["src"],
					"photo_url": imgtag["src"],
					"thumb_url": imgtag["src"]
					}
					if len(articles) > 14:
						break
					
					articles.append(curr_img)
			
			#articles = [{'type': 'article', 'id': 'abc', 'title': query_string, 'message_text': query_string}]
			return articles

		self.answerer.answer(msg, compute_answer)

	def on_chosen_inline_result(self, msg):
		pprint(msg)
		result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
		print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)

TOKEN = sys.argv[1]  # get token from command-line
bot = telepot.aio.DelegatorBot(TOKEN, [
	pave_event_space()(
		per_chat_id(), create_open, MessageCounter, timeout=10),
	pave_event_space()(
		per_inline_from_id(), create_open, InlineHandler, timeout=10),
])
loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')
loop.run_forever()