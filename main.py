from github import Github
from discord.ext import commands
import traceback

username = 'Soja8'

try:
	password = open('password.txt').read()
except:
	print("Can't find password file, aborting.")
	exit()

try:
	token = open('tokenfile.txt').read()
except:
	print("Can't find token file, aborting.")
	exit()

g = Github(username, password)



bot = commands.Bot(command_prefix='!git ') # add a space in the prefix
bot.remove_command('help') # remove command so that we can make our own

@bot.event
async def on_ready():
	channel = bot.get_channel(575153311259557915)
	await channel.send('Github bot"s up')

@bot.command()
async def help(ctx):
	await ctx.send("lol i aint gonna help you")


"""
@bot.event
async def on_message(message):
	
	if message.author == bot.user:
		return

	channel = bot.get_channel(575153311259557915)

	await channel.send(f'{message.author} said: {message.content}')
"""


bot.run(token, bot=True)
