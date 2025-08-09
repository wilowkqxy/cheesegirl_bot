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
back_markup.add(types.InlineKeyboardButton(text=back_btn_msg,callback_data="back"))

close_markup = types.InlineKeyboardMarkup()
close_markup.add(types.InlineKeyboardButton(text=close_btn_msg,callback_data="close"))

users = {}
aiMode = []
ideasMode = []

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
	try:
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
	except Exception as e:
		return ai_error_msg+str(e)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	with open("assets/starter.png","rb") as pic:
		if call.data == "discord":
			if call.from_user.id in users.keys():
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=discord_msg,reply_markup=back_markup)
				return
		elif call.data == "tg":
			if call.from_user.id in users.keys():
				#bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				#botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=tg_msg,reply_markup=back_markup)
				#users[call.from_user.id] = botmsg.message_id
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=tg_msg,reply_markup=back_markup)
				return
		elif call.data == "about":
			if call.from_user.id in users.keys():
				#bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				#botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=about_msg,reply_markup=back_markup)
				#users[call.from_user.id] = botmsg.message_id
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=about_msg,reply_markup=back_markup)
				return
		elif call.data == "ideas":
			if call.from_user.id in users.keys():
				if call.from_user.id not in ideasMode:
					ideasMode.append(call.from_user.id)

				with open("assets/ideas.jpg","rb") as pic:
					bot.edit_message_media(chat_id=call.from_user.id,message_id=users[call.from_user.id],media=types.InputMediaPhoto(pic),reply_markup=back_markup)
					bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=ideas_prompt_msg,reply_markup=back_markup)

		elif call.data == "ai":
			if call.from_user.id in users.keys():
				if call.from_user.id not in aiMode:
					aiMode.append(call.from_user.id)
				#bot.delete_message(chat_id=call.from_user.id,message_id=users[call.from_user.id])
				#botmsg = bot.send_photo(chat_id=call.from_user.id,photo=pic,caption=ai_prompt_msg,reply_markup=back_markup)
				#users[call.from_user.id] = botmsg.message_id
				bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=ai_prompt_msg,reply_markup=back_markup)
				return
		elif call.data == "close":
			if call.message:
				try:
					bot.delete_message(chat_id=call.from_user.id,message_id=call.message.message_id)
				except:
					print("lol, an error occured while closing message 😭😭")
		elif call.data == "idea_like":
			if call.message and call.message.chat.id == ideas_group_id:
				try:
					op = int(call.message.text.split(".f.")[1])
					splitted = call.message.text.split("\n\n")

					voted = splitted[2]
					votedList = voted.split(",i")

					for user in votedList:
						if str(user) == str(call.from_user.id):
							return

					if len(votedList) <= 1:
						votedList = []
						voted += f",i{call.from_user.id}"
					else:
						voted += f",i{call.from_user.id}"

					votedList.append(call.from_user.id)

					rating = int(splitted[1])
					rating += 1
					print(f"rating: {rating}")

					idea = splitted[4]

					markup = types.InlineKeyboardMarkup()

					like_btn = types.InlineKeyboardButton(text="✅",callback_data="idea_like")
					dislike_btn = types.InlineKeyboardButton(text="❌",callback_data="idea_dislike")

					markup.add(like_btn,dislike_btn)

					if rating >= 3:
						print(f"idea from {op} is approved")
						bot.edit_message_text(chat_id=ideas_group_id,text=f""".f.{op}.f.\n\n{rating}\n\n{voted}\n\n{ideas_newidea_msg} tg://user?id={op} @{bot.get_chat(op).username} <- если это None то у чела нету юза лолкек:


{idea}

{ideas_status_approved_msg}""",message_id=call.message.message_id)

						with open("assets/ideas.jpg","rb") as pic:
							bot.send_photo(chat_id=op,photo=pic,caption=f"{ideas_approved_msg}	{idea}\n\n{ideas_approved_msg_2}",reply_markup=close_markup)

						return

					bot.edit_message_text(chat_id=ideas_group_id,text=f""".f.{op}.f.\n\n{rating}\n\n{voted}\n\n{ideas_newidea_msg} tg://user?id={op} @{bot.get_chat(op).username} <- если это None то у чела нету юза лолкек:

{idea}""",message_id=call.message.message_id,reply_markup=markup)
				except Exception as e:
					with open("assets/error.jpg","rb") as pic:
						bot.send_photo(chat_id=call.message.chat.id,photo=pic,caption=ai_error_msg+str(e),reply_markup=close_markup)
		elif call.data == "idea_dislike":
			if call.message and call.message.chat.id == ideas_group_id:
				try:
					op = int(call.message.text.split(".f.")[1])
					splitted = call.message.text.split("\n\n")

					voted = splitted[2]
					votedList = voted.split(",i")

					for user in votedList:
						if str(user) == str(call.from_user.id):
							return

					if len(votedList) <= 1:
						votedList = []
						voted += f",i{call.from_user.id}"
					else:
						voted += f",i{call.from_user.id}"

					votedList.append(call.from_user.id)

					rating = int(splitted[1])
					rating -= 1
					print(f"rating: {rating}")

					idea = splitted[4]

					markup = types.InlineKeyboardMarkup()

					like_btn = types.InlineKeyboardButton(text="✅",callback_data="idea_like")
					dislike_btn = types.InlineKeyboardButton(text="❌",callback_data="idea_dislike")

					markup.add(like_btn,dislike_btn)

					if rating <= -2:
						print(f"idea from {op} is not approved")
						bot.edit_message_text(chat_id=ideas_group_id,text=f""".f.{op}.f.\n\n{rating}\n\n{voted}\n\n{ideas_newidea_msg} tg://user?id={op} @{bot.get_chat(op).username} <- если это None то у чела нету юза лолкек:


{idea}

{ideas_status_notapproved_msg}""",message_id=call.message.message_id)

						with open("assets/ideas.jpg","rb") as pic:
							bot.send_photo(chat_id=op,photo=pic,caption=f"{ideas_notapproved_msg}	{idea}\n\n{ideas_notapproved_msg_2}",reply_markup=close_markup)

						return

					bot.edit_message_text(chat_id=ideas_group_id,text=f""".f.{op}.f.\n\n{rating}\n\n{voted}\n\n{ideas_newidea_msg} tg://user?id={op} @{bot.get_chat(op).username} <- если это None то у чела нету юза лолкек:

{idea}""",message_id=call.message.message_id,reply_markup=markup)
				except Exception as e:
					with open("assets/error.jpg","rb") as pic:
						bot.send_photo(chat_id=call.message.chat.id,photo=pic,caption=ai_error_msg+str(e),reply_markup=close_markup)


		elif call.data == "back":
			if call.from_user.id in aiMode:
				aiMode.remove(call.from_user.id)
			if call.from_user.id in ideasMode:
				ideasMode.remove(call.from_user.id)



			markup = types.InlineKeyboardMarkup()

			discord_button = types.InlineKeyboardButton(
				text = discord_btn_msg,
				callback_data = "discord"
			)
			tg_button = types.InlineKeyboardButton(
				text = tg_btn_msg,
				callback_data = "tg"
			)
			about_button = types.InlineKeyboardButton(
				text = about_btn_msg,
				callback_data = "about"
			)
			ideas_button = types.InlineKeyboardButton(
				text = ideas_btn_msg,
				callback_data = "ideas"
			)
			ai_button = types.InlineKeyboardButton(
				text = ai_btn_msg,
				callback_data = "ai"
			)

			user_full = call.from_user.first_name

			if call.from_user.last_name:
				user_full += " " + call.from_user.last_name

			markup.add(discord_button)
			markup.add(tg_button)
			markup.add(about_button)
			markup.add(ideas_button)
			markup.add(ai_button)

			with open("assets/starter.png","rb") as pic:
				if call.from_user.id in users.keys():
					if call.from_user.id in inAiChat:
						inAiChat.remove(call.from_user.id)

						bot.edit_message_media(chat_id=call.from_user.id,message_id=users[call.from_user.id],media=types.InputMediaPhoto(pic))
						bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=f"{start_msg_1}{user_full}! " + start_msg,reply_markup=markup)

						return

					bot.edit_message_caption(chat_id=call.from_user.id,message_id=users[call.from_user.id],caption=f"{start_msg_1}{user_full}! " + start_msg,reply_markup=markup)
				else:
					botmsg = bot.send_photo(call.from_user.id,photo=pic,caption=f"{start_msg_1}{user_full}! "+start_msg,reply_markup=markup)
					users[call.from_user.id] = botmsg.message_id

@bot.message_handler(commands=['start'])
def start(msg):
	print(f"bot started from {msg.chat.id}")
	#if msg.from_user.id in users.keys():
	#	return

	if msg.from_user.id in aiMode:
		aiMode.remove(msg.from_user.id)
	if msg.from_user.id in ideasMode:
		ideasMode.remove(msg.from_user.id)
	if msg.from_user.id in inAiChat:
		inAiChat.remove(msg.from_user.id)

	markup = types.InlineKeyboardMarkup()

	discord_button = types.InlineKeyboardButton(
		text = discord_btn_msg,
		callback_data = "discord"
	)
	tg_button = types.InlineKeyboardButton(
		text = tg_btn_msg,
		callback_data = "tg"
	)
	about_button = types.InlineKeyboardButton(
		text = about_btn_msg,
		callback_data = "about"
	)
	ideas_button = types.InlineKeyboardButton(
		text = ideas_btn_msg,
		callback_data = "ideas"
	)
	ai_button = types.InlineKeyboardButton(
		text = ai_btn_msg,
		callback_data = "ai"
	)

	user_full = msg.from_user.first_name

	if msg.from_user.last_name:
		user_full += " " + msg.from_user.last_name

	markup.add(discord_button)
	markup.add(tg_button)
	markup.add(about_button)
	markup.add(ideas_button)
	markup.add(ai_button)

	with open("assets/starter.png","rb") as pic:
		botmsg = bot.send_photo(msg.from_user.id,photo=pic,caption=f"{start_msg_1}{user_full}! "+start_msg,reply_markup=markup)
		users[msg.from_user.id] = botmsg.message_id

	bot.delete_message(chat_id=msg.from_user.id,message_id=msg.message_id)

	print(users[msg.from_user.id])

@bot.message_handler()
def domsg(msg):
	if msg.content_type == "text":
		if msg.from_user.id in aiMode:
			try:
				if msg.from_user.id not in inAiChat:
					inAiChat.append(msg.from_user.id)

				if datetime.now(timezone.utc).hour+3 <= 9 and datetime.now(timezone.utc).hour+3 >= 21: # спит с 21:00 до 9:00 (UTC+3)
				#if true:
					if wake_up_msg in msg.text.lower():
						with open("assets/thinking_sleepy.png","rb") as pic:
							#bot.delete_message(chat_id=msg.from_user.id,message_id=users[msg.from_user.id])
							#botmsg = bot.send_photo(chat_id=msg.from_user.id,photo=pic,caption=thinking_msg,reply_markup=back_markup)
							#users[msg.from_user.id] = botmsg.message_id
							bot.edit_message_media(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],media=types.InputMediaPhoto(pic))
							bot.edit_message_caption(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],caption=thinking_msg)

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
							#bot.delete_message(chat_id=msg.from_user.id,message_id=users[msg.from_user.id])
							#botmsg = bot.send_photo(chat_id=msg.from_user.id, photo=pic,caption=sleep_mask,reply_markup=back_markup)
							#users[msg.from_user.id] = botmsg.message_id
							bot.edit_message_media(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],media=types.InputMediaPhoto(pic))
							bot.edit_message_caption(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],caption=sleep_mask,reply_markup=back_markup)
							return
				else:
					with open("assets/thinking.png","rb") as pic:
						#bot.delete_message(chat_id=msg.from_user.id,message_id=users[msg.from_user.id])
						#botmsg = bot.send_photo(chat_id=msg.from_user.id,photo=pic,caption=thinking_msg,reply_markup=back_markup)
						#users[msg.from_user.id] = botmsg.message_id
						bot.edit_message_media(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],media=types.InputMediaPhoto(pic))
						bot.edit_message_caption(chat_id=msg.from_user.id,message_id=users[msg.from_user.id],caption=thinking_msg,reply_markup=back_markup)

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
			except Exception as e:
				with open("assets/error.jpg","rb") as pic:
					bot.send_photo(chat_id=msg.from_user.id,photo=pic,caption=ai_error_msg+str(e),reply_markup=close_markup)
		elif msg.from_user.id in ideasMode:
			try:
				markup = types.InlineKeyboardMarkup()

				like_btn = types.InlineKeyboardButton(text="✅",callback_data="idea_like")
				dislike_btn = types.InlineKeyboardButton(text="❌",callback_data="idea_dislike")

				markup.add(like_btn,dislike_btn)

				#for lox in sukakaketonazvatList:
				bot.send_message(chat_id=ideas_group_id,text=f".f.{msg.from_user.id}.f.\n\n0\n\n\n\n{ideas_newidea_msg} tg://user?id={msg.from_user.id} @{bot.get_chat(msg.from_user.id).username} <- если это None то у чела нету юза лолкек:\n\n{msg.text}",reply_markup=markup)

				custom_markup = types.InlineKeyboardMarkup()
				custom_markup.add(types.InlineKeyboardButton(text=close_btn_msg,callback_data="back"))

				ideasMode.remove(msg.from_user.id)

				bot.edit_message_caption(chat_id=msg.from_user.id,caption=ideas_sent_msg,message_id=users[msg.from_user.id],reply_markup=custom_markup) # sent
			except Exception as e:
				with open("assets/error.jpg","rb") as pic:
					bot.send_photo(chat_id=msg.from_user.id,photo=pic,caption=ai_error_msg+str(e),reply_markup=close_markup)
		elif msg.text.lower() == tomat_msg:
			bot.edit_message_caption(chat_id=msg.from_user.id,caption=tomat_response_msg,message_id=users[msg.from_user.id],reply_markup=back_markup)
	bot.delete_message(msg.from_user.id,msg.message_id)


bot.infinity_polling()
