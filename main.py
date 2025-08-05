#!/usr/bin/python3

import telebot
import requests
import random

from telebot import types
from datetime import datetime, timezone

from lang import *
from supersecret import *

model_ai = "gemini-2.5-flash"
GOOGLE_GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model_ai}:generateContent"

users = {}

aiMode = []

back_markup = types.InlineKeyboardMarkup()
back_markup.add(types.InlineKeyboardButton(text="↩️ назад",callback_data="back"))

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
	if call.data == "discord":
		if call.from_user.id in users.keys():
			bot.edit_message_text(chat_id=call.from_user.id,text=discord_msg,message_id=users[call.from_user.id],reply_markup=back_markup)
			return
		bot.send_message(call.from_user.id,discord_msg,reply_markup=back_markup)
	elif call.data == "tg":
		if call.from_user.id in users.keys():
			bot.edit_message_text(chat_id=call.from_user.id,text=tg_msg,message_id=users[call.from_user.id],reply_markup=back_markup)
			return
		bot.send_message(call.from_user.id,tg_msg,reply_markup=back_markup)
	elif call.data == "about":
		if call.from_user.id in users.keys():
			bot.edit_message_text(chat_id=call.from_user.id,text=about_msg,message_id=users[call.from_user.id],reply_markup=back_markup)
			return
	elif call.data == "ai":
		if call.from_user.id in users.keys():
			if call.from_user.id not in aiMode:
				aiMode.append(call.from_user.id)
			bot.edit_message_text(chat_id=call.from_user.id,text=ai_prompt_msg,message_id=users[call.from_user.id],reply_markup=back_markup)
			return
	elif call.data == "back":
		if call.from_user.id in aiMode:
			aiMode.remove(call.from_user.id)

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
			botmsg = bot.edit_message_text(chat_id=call.from_user.id,text=f"👋 Приветствую {user_full}! " + start_msg,message_id=users[call.from_user.id],reply_markup=markup)

			users[call.from_user.id] = botmsg.message_id


			return
		botmsg = bot.send_message(call.from_user.id,f"👋 Приветствую {user_full}! " + start_msg,reply_markup=markup)

		users[call.from_user.id] = botmsg.message_id

@bot.message_handler(commands=['start'])
def start(msg):
	#if msg.from_user.id in users.keys():
	#	return

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

	botmsg = bot.send_message(msg.from_user.id,f"👋 Приветствую {user_full}! " + start_msg,reply_markup=markup)
	users[msg.from_user.id] = botmsg.message_id

	print(users[msg.from_user.id])

@bot.message_handler()
def domsg(msg):
	if msg.content_type == "text":
		if msg.from_user.id in aiMode:
			if datetime.now(timezone.utc).hour < 6 and datetime.now(timezone.utc).hour < 21:
				if "разбудить сырный соус тян" in msg.text.lower():
					#angry = all(word not in msg.text.lower() for word in badwords)

					#for word in badwords:
					#	if word in msg.text.lower():
					#		angry = True
					#		break

					angry = any(word in msg.text.lower() for word in badwords)

					response = getAIResponse(msg.text+sleepy_mask)

					if angry:
						with open("assets/angry_sleepy.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)

					if random.randint(1,2) == 1 and not angry:
						with open("assets/sleepy.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
					else:
						if not angry:
							with open("assets/sleepy_2.png","rb") as pic:
								bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
				else:
					response = sleep_mask
					with open("assets/sleep.png","rb") as pic:
						bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
			else:
				#angry = True

				#for i in range(1,len(badwords)):
				#	if badwords[i] in msg.text.lower():
				#		angry = True
				#		break

				#for word in badwords:
				#	if word in msg.text.lower():
				#		angry = True
				#		break

				#angry = all(word not in msg.text.lower() for word in badwords)

				angry = any(word in msg.text.lower() for word in badwords)

				print(f"bad word detected: {angry}")

				response = getAIResponse(msg.text)

				if random.randint(1,2) == 1:
					if angry:
						with open("assets/angry.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
					else:
						with open("assets/default.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
				else:
					if angry:
						with open("assets/angry_2.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)
					else:
						with open("assets/default_2.png","rb") as pic:
							bot.edit_message_media(chat_id=msg.from_user.id, media=types.InputMediaPhoto(pic) , message_id=users[msg.from_user.id],reply_markup=back_markup)

			bot.edit_message_caption(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],caption=response)

		elif msg.text.lower() == "томат":
			bot.edit_message_text(chat_id=msg.from_user.id,text="""Вас инфицировали
Теперь вы должны написать в описании пользователя "Напиши мне в ЛС слово Томат"
Инфекция должна распространяться тихо
Единственное правило - не спойлерить игру другим и не говорить заранее, что будет, если они напишут слово томат""",message_id=users[msg.from_user.id],reply_markup=back_markup)


bot.infinity_polling()
