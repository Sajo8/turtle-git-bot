from github import Github
from discord.ext import commands

# todo actually do the stuff bruh

try:
	username = 'Soja8'
	password = open('password.txt').read()
	token = open('tokenfile.txt').read()
except:
	print("Can't find password/token file, aborting.")
	exit()

g = Github(username, password) # log into github my g

bot = commands.Bot(command_prefix='.git ') # add a space in the prefix
bot.remove_command('help') # remove command so that we can make our own

reserved_commands = ['help'] # list of the commands we make

def msg_not_in_list_of_commands(ctx):
	return str(ctx.command) not in reserved_commands # return true if the command passed is not in the list of reserved ones

@bot.event
async def on_ready():
	channel = bot.get_channel(575153311259557915)
	await channel.send("Github bot's up") # when ready send a confirmation message

@bot.command()
async def help(ctx): # help message on ".git help"
	await ctx.send("Bot underworks, help message coming promptly!")

@bot.event
async def on_message(message):
	
	if message.author == bot.user: # if the bot said it ignore
		return
	
	ctx = await bot.get_context(message) # get context

	if msg_not_in_list_of_commands(ctx): # if command not in reserved ones
		# just do whatever
		channel = ctx.channel 
		await channel.send(f'{ctx.author} said: {ctx.message.content}')
	else:
		if ctx.valid: await bot.invoke(ctx) # otherwise call appropriate command function(if valid)

bot.run(token, bot=True)