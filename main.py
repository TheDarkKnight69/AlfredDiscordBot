import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
bad_words = ["fuck", "cunt"]
happy_words = ["pog", "amazing", "ily", "happy", "wholesome", "best"]
reaction = ['<:ducklove:955328384546791455>','<:Milk_Mocha:955335754131841035>', '<:milk_mocha_hug:955336262926082089>', '<:mochaBear:955336309310890005>', '<:MilkMochaUltraLove:955336409621872670>', '<:mocha_milkdinolove:955336957666402374>', '<:chickjump:955337328413528125>' ]


starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are an amazing person!"
]

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


def get_insult():
  response = requests.get("https://insult.mattbas.org/api/insult.json")
  json_data = json.loads(response.text)
  insult = json_data
  return(insult)


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def get_shibe():
  response = requests.get("http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true")
  json_data = json.loads(response.text)
  shibe = json_data
  return(shibe)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith("!new"):
    encouraging_message = msg.split("!new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements.value)

  if msg.startswith("!list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements.value)

  if msg.startswith("!responding"):
    value = msg.split("! responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if msg.startswith("!status"):
      await message.channel.send("We're at 120 lines of code now pog!!")
  
  if msg.startswith("!who are you"):
      await message.channel.send("I am a simple bot with very less functions which searches for sad words and returns an encouraging message. Also i give cool inspirational thingies. :D")
    
  if msg.startswith("!hello"):
      await message.channel.send("Hello!!", mention_author=True)

  if msg.startswith("!insult"):
    insult = get_insult
    await message.channel.send(insult)
  
  if msg.startswith("!shibe"):
    shibe = get_shibe
    await message.channel.send(shibe)

  if any(word in message.content for word in bad_words):
    await message.delete(delay=2)
    
  if any(word in message.content for word in happy_words):
    await message.add_reaction(random.choice(reaction))

  if msg.startswith("!nuke"):
    await message.channel.delete()

  if msg.startswith("!test"):
    await message.channel.send(discord.Guild.fetch_emojis(discord.Emojis))
    
keep_alive()

client.run(os.getenv('TOKEN'))