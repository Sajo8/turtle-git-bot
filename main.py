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

#reserved_commands = ['help', 'makeissue'] # list of the commands we make

@bot.event
async def on_ready():
	channel = bot.get_channel(575153311259557915)
	await channel.send("Github bot's up") # when ready send a confirmation message

@bot.command()
async def makeissue(ctx): # we makin an issue bois
	
	await ctx.send("It seems you'd like to make an issue! Let's continue. Say `.git cancel` at any time to cancel the process.")
	await ctx.send("**Please enter the name of the repository in which you'd like to make an issue!** \n*Eg: `.git turtlecoin-wallet-electron`*")

	def check(m):
		return m.channel == ctx.channel and m.author == ctx.author
	
	repo_name = None
	while not repo_name:
		repo_name = await bot.wait_for('message', check=check)
		print(repo_name.content)

# TODO: fix up this so that it ensures the checks
# not reserved commands
# cancel if a cancel command
# wont go wack if called multiple times
# etc

@bot.command()
async def help(ctx): # help message on ".git help"
	await ctx.send("help msg coming soon")

@bot.event
async def on_command_error(ctx, error):
	pass # get rid of command errors
	# this is called all the time whenver the user does `.git whatever`
	# ugly when its being used for the title or whatever

"""
@bot.event
async def on_message(message):
	
	if message.author == bot.user: # if the bot said it ignore
		return
	
	ctx = await bot.get_context(message) # get context

	if str(ctx.command) not in reserved_commands: # if command not in reserved ones
		channel = ctx.channel 
		await channel.send(f'{ctx.author} said: {ctx.message.content}')
	else:
		if ctx.valid: await bot.invoke(ctx) # otherwise let appropriate command run
"""

bot.run(token, bot=True)