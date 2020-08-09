import os
import discord
import random
import requests
import json
import html

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

quotes = ['ur gay', 'shut up', 'fuck you seth']
x = {}

def print_question(question, answers):
    text_ = str(html.unescape(question))
    text_ += '\n'

    count = 1
    for q in answers:
        text_ += str(count) + ') ' + str(html.unescape(q)) + '\n'
        count += 1

    return text_

def getQuestion():
    url = 'https://opentdb.com/api.php'

    params = {'amount': '1', 'difficulty': 'medium', 'type': 'multiple'}

    response = requests.get(url, params=params)

    result = json.loads(response.text)['results'][0]

    answer_list = result['incorrect_answers']
    answer_list.append(result['correct_answer'])

    print(answer_list)
    random.shuffle(answer_list)
    print(answer_list)

    return {'question': result['question'], 'answers': answer_list, 'correct': result['correct_answer']}

def getInsult(name):
    url = 'https://insult.mattbas.org/api/insult'

    params = {}

    response = requests.get(url, params=params)

    return response.text



@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'go!':
        await message.channel.send(getInsult(message.author))

    elif message.content == 'now!':
        result = getQuestion()
        x.update({'answer': result['correct']})
        x.update({'number': result['answers'].index(result['correct']) + 1})
        await message.channel.send(print_question(result['question'], result['answers']))

    if x:
        if message.content == x['answer'] or message.content == str(x['number']):
            x.clear()
            await message.channel.send('BIG BRAIN 5 HEAD MONSTER')
            await message.channel.send(str(message.author).split('#')[0])

client.run(TOKEN)

