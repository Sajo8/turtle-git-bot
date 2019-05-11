# TODO
# Make sure makeissue can't be called multiple times
# Cancel everything when .git cancel is called
# Do the issue title and issue body part
# Make the issue
# Catch errors, return descriptive ones

from github import Github
from discord.ext import commands
import threading
import traceback

try:
	username = 'Soja8'
	password = open('password.txt').read()
	token = open('tokenfile.txt').read()
except:
	print("Can't find password/token file, aborting.")
	exit()

g = Github(username, password) # log into github my g
g_org = g.get_organization("TurtleCoin")
g_org_repos = None

timeout = 10.0 # 10 seconds 1 day = 86400

bot = commands.Bot(command_prefix='.git ') # add a space in the prefix
bot.remove_command('help') # remove command so that we can make our own

__TEST_MODE = True

#reserved_commands = ['help', 'makeissue'] # list of the commands we make

def get_org_repos():
	global g_org_repos
	t = threading.Timer(10,0, get_org_repos)
	t.start()
	g_org_repos = g_org.get_repos()

t = threading.Timer(10.0, get_org_repos)
t.start()

async def check_if_repo_valid(repo_name, ctx):
	await ctx.send("Checking...")
	# if the repo_name is in the list of repos, then it's True. otherwise it's not
	for repo in g_org_repos:
		g_repo_name = repo.name
		if repo_name == g_repo_name:
			return True
	return False


async def get_repo_name(ctx):

	def check(m):
		return m.channel == ctx.channel and m.author == ctx.author and m.content.startswith(".git")
	
	repo_name = None
	
	await ctx.send("**Please enter the name of the repository in which you'd like to make an issue!** \n*Eg: `.git turtlecoin-wallet-electron`*")

	repo_name = await bot.wait_for('message', check=check)
	repo_name = repo_name.content[5:]

	if __TEST_MODE: # return it w/out checking since just testing
		return repo_name
	
	if await check_if_repo_valid(repo_name, ctx): # it's all good
		return repo_name
	else: # invalid, return false and quit
		await ctx.send("**Invalid repo name!** Quitting, please re-make your issue") # TODO: let the user continue where he left off.
		return False


@bot.event
async def on_ready():
	channel = bot.get_channel(575153311259557915)
	await channel.send("Github bot's up") # when ready send a confirmation message

@bot.command()
async def makeissue(ctx): # we makin an issue bois
	
	await ctx.send("It seems you'd like to make an issue! Let's continue. Say `.git cancel` at any time to cancel the process.")

	repo_name = await get_repo_name(ctx)
	if not repo_name: # if the name is invalid, quit
		return
	await ctx.send("**Valid repo name!** Let's continue")

	# do the rest

@bot.command()
async def help(ctx): # help message on ".git help"
	await ctx.send("help msg coming soon")

@bot.event
async def on_command_error(ctx, error):
	print(error)
	traceback.print_exc()
	#pass # get rid of command errors
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