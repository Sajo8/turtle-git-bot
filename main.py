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

g = Github(username, password) # log into github my g
github_org = g.get_organization("TurtleCoin")
github_org_repos = None

bot = commands.Bot(command_prefix='.git ') # add a space in the prefix
bot.remove_command('help') # remove command so that we can make our own

bot.making_issue = False
bot._HELP_MSG = """\
**TurtleCoin GitHub Bot**
Commands:
```
.git help:      Show this message
.git makeissue: Make an issue
.git cancel:    Cancel any issue being made 
```"""

bot.__TEST_MODE = False # used to bypass any checks

bot.reserved_commands = ['help', 'makeissue', 'ev'] # commands which do not count as repo_names or stuff like that
# cancel is not included since we need to check that seperately

##############
# Timer which keeps getting repo names
# Runs once, then repeats once every day

class BackgroundTimer(Thread):
    def get_org_repos(self):
        global github_org_repos
        bot.github_org_repos = github_org.get_repos()
    def run(self):
        while True:
            self.get_org_repos()
            time.sleep(86400) # sleep for one day

timer = BackgroundTimer()
timer.start()

##############

@bot.event
async def on_ready():
    channel = bot.get_channel(575153311259557915)
    await channel.send("Github bot's up") # when ready send a confirmation message

@bot.command()
async def makeissue(ctx): # we makin an issue bois  

    # already in the process of making an issue, just stop
    if bot.making_issue:
        await ctx.send("Already making issue! Say `.git cancel` to cancel current process.")
        return
    
    # weren't before, but now we are!
    bot.making_issue = True

    await ctx.send("It seems you'd like to make an issue! Let's continue. Say `.git cancel` at any time to cancel the process.")

    repo_name = None
    repo_name = await get_repo_name(ctx, bot) # get repo name

    if not repo_name: # if it is returned false, then just exit
        bot.making_issue = False # not making issue anymore
        return

    # set it to false, done making issue    
    bot.making_issue = False 

@bot.command()
async def help(ctx): # help message on ".git help"
    await ctx.send(bot._HELP_MSG)

@bot.command()
async def cancel(ctx): # just says "Cancelling" lol, the real work is done separately for each part
    await ctx.send("Cancelling...")

@bot.command()
async def ev(ctx, arg): # print out value of given var
    if ctx.author.id != 235707623985512451: # only me hahha
        await ctx.send('Sorry, only the owner of the bot can use this command!')
        return
    try: # check globals
        await ctx.send(globals()[arg])
    except KeyError: # not in globals
        args = arg.split('.')
        v = vars(bot)
        ar = args[1]
        await ctx.send(f'{arg}: {v[ar]}')
    except Exception as e: # catch all
        await ctx.send(f'Some error occured: {e}')



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