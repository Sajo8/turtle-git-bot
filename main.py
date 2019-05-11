from github import Github
from discord.ext import commands
from threading import Thread
import time
import traceback

from reponame import get_repo_name

try:
    username = 'Soja8'
    password = open('password.txt').read()
    token = open('tokenfile.txt').read()
except:
    print("Can't find password/token file, aborting.")
    exit()

_HELP_MSG = """\
**TurtleCoin GitHub Bot**
Commands:
```
.git help:      Show this message
.git makeissue: Make an issue
.git cancel:    Cancel any issue being made 
```"""


g = Github(username, password) # log into github my g
github_org = g.get_organization("TurtleCoin")
github_org_repos = None

bot = commands.Bot(command_prefix='.git ') # add a space in the prefix
bot.remove_command('help') # remove command so that we can make our own

__TEST_MODE = False
bot.__TEST_MODE = False # make a botvar to pass data between modules

#reserved_commands = ['help', 'makeissue'] # list of the commands we make

##############
# Timer which keeps getting repo names
# Runs once, then repeats once every day

class BackgroundTimer(Thread):
    def get_org_repos(self):
        global github_org_repos
        github_org_repos = github_org.get_repos()
        bot.github_org_repos = github_org_repos
    def run(self):
        while True:
            self.get_org_repos()
            time.sleep(86400) # sleep for one day

timer = BackgroundTimer()
timer.start()
#
#
##############

@bot.event
async def on_ready():
    channel = bot.get_channel(575153311259557915)
    await channel.send("Github bot's up") # when ready send a confirmation message

@bot.command()
async def makeissue(ctx): # we makin an issue bois
    
    await ctx.send("It seems you'd like to make an issue! Let's continue. Say `.git cancel` at any time to cancel the process.")

    repo_name = None
    repo_name = await get_repo_name(ctx, bot)
    if not repo_name: # if it is returned false, then just exit
        return

@bot.command()
async def help(ctx): # help message on ".git help"
    await ctx.send(_HELP_MSG)

"""
@bot.event
async def on_command_error(ctx, error):
    print(error)
    traceback.print_exc()
    #pass # get rid of command errors
    # this is called all the time whenver the user does `.git whatever`
    # ugly when its being used for the title or whatever
"""

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