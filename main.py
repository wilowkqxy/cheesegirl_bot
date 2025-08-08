#!/usr/bin/python3

import sys

try:
	import telebot
	import requests
	import random
	import json
	import threading

	from telebot import types
	from datetime import datetime, timezone

	from lang import *
	from supersecret import *
except Exception as e:
	print(f"FATAL ERROR WHILE IMPORTING: {str(e)}")
	sys.exit(1)

model_ai = "gemini-2.5-flash"
GOOGLE_GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model_ai}:generateContent"

back_markup = types.InlineKeyboardMarkup()
back_markup.add(types.InlineKeyboardButton(text="↩️ назад",callback_data="back"))

users = {}
aiMode = []

inAiChat = []

#dataLoadFailed = False

#try:
#	with open("data.json","r") as data:
#		userdata = json.load(data)
#
#		users = userdata.get("users",{})
#		aiMode = userdata.get("aiMode",[])
#except Exception as e:
#	dataLoadFailed = True
#	print(f"failed to load userdata, loading with default values: {str(e)}")
#	users = {}
#	aiMode = []

#print(users)
#print(aiMode)

#def autoSave():
#	print("auto saving...")
#	try:
#		if dataLoadFailed:
#			return
#		else:
#			with open("data.json","w") as data:
#				userdata = {
#					"users": users,
#					"aiMode": aiMode
#				}
#
#				json.dump(userdata,data)
#
#			threading.Timer(30,autoSave).start()
#
#	except Exception as e:
#		print(f"failed to save data: {str(e)}")

#autoSave()

bot = telebot.TeleBot(SUPERSECRETTOKENLOL)

def getAIResponse(prompt):
	if not prompt:
		prompt = "привет"

	headers = {
		"Content-Type": "application/json",
	}
	params = {
		"key": api_key
	}
	payload = {
		"contents": [
			{
				"parts": [
					{"text": mask + prompt}
				]
			}
		]
	}
	response = requests.post(GOOGLE_GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=30)
	response.raise_for_status()

	content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
	return content

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	with open("assets/starter.png","rb") as pic:
		if call.data == "discord":
			if call.from_user.id in users.keys():
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=discord_msg,reply_markup=back_markup)
				return
			else:
				bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=discord_msg,reply_markup=back_markup)
				users[call.from_user.id] = botmsg.message_id
		elif call.data == "tg":
			if call.from_user.id in users.keys():
				#bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				#botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=tg_msg,reply_markup=back_markup)
				#users[call.from_user.id] = botmsg.message_id
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=tg_msg,reply_markup=back_markup)
				return
			else:
				bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=tg_msg,reply_markup=back_markup)
				users[call.from_user.id] = botmsg.message_id
		elif call.data == "about":
			if call.from_user.id in users.keys():
				#bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				#botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=about_msg,reply_markup=back_markup)
				#users[call.from_user.id] = botmsg.message_id
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=about_msg,reply_markup=back_markup)
				return
			else:
				bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=about_msg,reply_markup=back_markup)
				users[call.from_user.id] = botmsg.message_id
		elif call.data == "ai":
			if call.from_user.id in users.keys():
				if call.from_user.id not in aiMode:
					aiMode.append(call.from_user.id)
				#bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				#botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=ai_prompt_msg,reply_markup=back_markup)
				#users[call.from_user.id] = botmsg.message_id
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=ai_prompt_msg,reply_markup=back_markup)
				return
			else:
				if call.from_user.id not in aiMode:
					aiMode.append(call.from_user.id)

				bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=ai_prompt_msg,reply_markup=back_markup)
				users[call.from_user.id] = botmsg.message_id
		elif call.data == "back":
			markup = types.InlineKeyboardMarkup()

			discord_button = types.InlineKeyboardButton(
				text = "↪️ дискорд ссылка  ",
				callback_data = "discord"
			)
			tg_button = types.InlineKeyboardButton(
				text = "↪️ телеграм ссылка  ",
				callback_data = "tg"
			)
			about_button = types.InlineKeyboardButton(
				text = "❔ о нас  ",
				callback_data = "about"
			)
			ai_button = types.InlineKeyboardButton(
				text = "🗣 поговорить с сырный соус тян  ",
				callback_data = "ai"
			)

			user_full = call.from_user.first_name

			if call.from_user.last_name:
				user_full += " " + call.from_user.last_name

			markup.add(discord_button)
			markup.add(tg_button)
			markup.add(about_button)
			markup.add(ai_button)

			if call.from_user.id in users.keys():
				with open("assets/starter.png","rb") as pic:
					if call.from_user.id in aiMode:
						aiMode.remove(call.from_user.id)

					if call.from_user.id in inAiChat:
						inAiChat.remove(call.from_user.id)

						bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
						botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=start_msg,reply_markup=markup)
						users[call.from_user.id] = botmsg.message_id

						return
					else:
						bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=f"👋 Приветствую {user_full}! " + start_msg,reply_markup=markup)
						return

			with open("assets/starter.png","rb") as pic:
					botmsg = bot.send_photo(call.from_user.id,photo=pic,caption=f"👋 Приветствую {user_full}! " + start_msg,reply_markup=markup)
					users[call.from_user.id] = botmsg.message_id

@bot.message_handler(commands=['start'])
def start(msg):
	#if msg.from_user.id in users.keys():
	#	return

	if msg.from_user.id in aiMode:
		aiMode.remove(msg.from_user.id)

	if msg.from_user.id in inAiChat:
		inAiChat.remove(msg.from_user.id)

	markup = types.InlineKeyboardMarkup()

	discord_button = types.InlineKeyboardButton(
		text = "↪️ дискорд ссылка  ",
		callback_data = "discord"
	)
	tg_button = types.InlineKeyboardButton(
		text = "↪️ телеграм ссылка  ",
		callback_data = "tg"
	)
	about_button = types.InlineKeyboardButton(
		text = "❔ о нас  "  ,
		callback_data = "about"
	)
	ai_button = types.InlineKeyboardButton(
		text = "🗣 поговорить с сырный соус тян  ",
		callback_data = "ai"
	)

	user_full = msg.from_user.first_name

	if msg.from_user.last_name:
		user_full += " " + msg.from_user.last_name

	markup.add(discord_button)
	markup.add(tg_button)
	markup.add(about_button)
	markup.add(ai_button)

	with open("assets/starter.png","rb") as pic:
		botmsg = bot.send_photo(msg.from_user.id,photo=pic,caption=f"👋 Приветствую {user_full}! " + start_msg,reply_markup=markup)
		users[msg.from_user.id] = botmsg.message_id

	bot.delete_message(chat_id=msg.from_user.id,message_id=msg.message_id)

	print(users[msg.from_user.id])

@bot.message_handler()
def domsg(msg):
	if msg.content_type == "text":
		if msg.from_user.id in aiMode:
			sleep = False

			if msg.from_user.id not in inAiChat:
				inAiChat.append(msg.from_user.id)

			if datetime.now(timezone.utc).hour+3 <= 9 and datetime.now(timezone.utc).hour+3 >= 21: # спит с 22:00 до 9:00 (UTC+3)
			#if true:
				if "разбудить сырный соус тян" in msg.text.lower():
					with open("assets/thinking_sleepy.png","rb") as pic:
						bot.delete_message(chat_id=msg.from_user.id,message_id=users[msg.from_user.id])
						botmsg = bot.send_photo(chat_id=msg.from_user.id,photo=pic,caption=thinking_msg,reply_markup=back_markup)
						users[msg.from_user.id] = botmsg.message_id

					angry = any(word in msg.text.lower() for word in badwords)

					if angry:
						response = getAIResponse(msg.text+sleepy_mask+angry_mask)
					else:
						response = getAIResponse(msg.text+sleepy_mask)

					if angry:
						with open("assets/angry_sleepy.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
					else:
						with open(f"assets/sleepy_{random.randint(1,2)}.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
				else:
					with open("assets/sleep.png","rb") as pic:
						bot.delete_message(chat_id=msg.from_user.id,message_id=users[msg.from_user.id])
						botmsg = bot.send_photo(chat_id=msg.from_user.id, photo=pic,caption=sleep_mask,reply_markup=back_markup)
						users[msg.from_user.id] = botmsg.message_id
						return
			else:
				with open("assets/thinking.png","rb") as pic:
					bot.delete_message(chat_id=msg.from_user.id,message_id=users[msg.from_user.id])
					botmsg = bot.send_photo(chat_id=msg.from_user.id,photo=pic,caption=thinking_msg,reply_markup=back_markup)
					users[msg.from_user.id] = botmsg.message_id

				angry = any(word in msg.text.lower() for word in badwords)

				if angry:
					response = getAIResponse(msg.text+angry_mask)
				else:
					response = getAIResponse(msg.text)


				rng = random.randint(1,2)

				pic = open(f"assets/default_{rng}.png","rb")

				if angry:
					pic.close()
					pic = open(f"assets/angry_{rng}.png","rb")

				bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
				pic.close()

			bot.edit_message_caption(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],caption=ai_yourmsg_msg+msg.text+"\n\n"+ai_answer_msg+response,reply_markup=back_markup)

		elif msg.text.lower() == "томат":
			bot.delete_message(chat_id=msg.from_user.id,message_id=users[msg.from_user.id])
			botmsg = bot.send_message(chat_id=msg.from_user.id,text="""Вас инфицировали
Теперь вы должны написать в описании пользователя "Напиши мне в ЛС слово Томат"
Инфекция должна распространяться тихо
Единственное правило - не спойлерить игру другим и не говорить заранее, что будет, если они напишут слово томат""",reply_markup=back_markup)
			users[msg.from_user.id] = botmsg.message_id
	bot.delete_message(msg.from_user.id,msg.message_id)


bot.infinity_polling()
