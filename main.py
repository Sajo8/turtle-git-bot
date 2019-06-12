from github import Github
from discord.ext import commands
from threading import Thread
from time import sleep

from reponame import get_repo_name
from issuetitle import get_issue_title
from issuebody import get_issue_body
from waitforconf import confirmdetails
from creategitissue import createissue

# try to get tokenfile and password
# we don't need the password but try anyways just to check
# then we delete it
try:
    password = open('password.txt').read()
    token = open('tokenfile.txt').read()
    del password
except:
    print("Can't find password/token file, aborting.")
    exit()

g = Github()
github_org = g.get_organization("TurtleCoin") # get turtlecoin org
github_org_repos = None

bot = commands.Bot(command_prefix='.git ') # set prefix
bot.remove_command('help') # remove command so that we can make our own

bot.making_issue = False

bot.__TEST_MODE = False # used to bypass any checks and make issue in test repo
bot.reserved_commands = ['help', 'makeissue', 'ev', 'status'] # commands which do not count as repo_names or stuff like that
# cancel is not included since we need to check that seperately

bot.issue_maker_author = None # used to ensure a couple of checks regarding op of message
bot.full_username = None # status msg and in github issue

# vars used to make issue
bot.repo_name = None
bot.issue_title = None
bot.issue_body = None

# time after which a message is auto deleteed
# 1 minute
bot.delete_delay = 60.0

# TurtleCoin, jc5Traq
allowed_servers = [388915017187328002]

##############
# Timer which keeps getting repo names
# Runs once, then repeats once every day
# Runs on a separate thread and doesn't interfere

class BackgroundTimer(Thread):
    def get_org_repos(self):
        global github_org_repos
        bot.github_org_repos = github_org.get_repos()
    def run(self):
        while True:
            self.get_org_repos()
            sleep(86400) # sleep for one day

timer = BackgroundTimer()
timer.start()

##############

@bot.event
async def on_ready():
    channel = bot.get_channel(401109818607140864)
    await channel.send("Github bot's up") # when ready send a confirmation message
    print("Bot up!")

@bot.event
async def on_guild_join(guild):
    if guild.id not in allowed_servers:
        guild.leave()

@bot.command()
async def makeissue(ctx): # we makin an issue bois

    await ctx.message.delete(delay=bot.delete_delay)

    # already in the process of making an issue, just stop
    if bot.making_issue:
        await ctx.send("Already making issue! Say `.git cancel` to cancel current process.", delete_after=bot.delete_delay)
        return

    # weren't before, but now we are!
    bot.making_issue = True
    # save author id
    bot.issue_maker_author = ctx.author.id
    # create a full username
    user_info = await bot.fetch_user(bot.issue_maker_author)
    bot.full_username = f"@{user_info.name}#{user_info.discriminator}"


    await ctx.send("It seems you'd like to make an issue! Let's continue. Say `.git cancel` at any time to cancel the process.", delete_after=bot.delete_delay)

    bot.repo_name = await get_repo_name(ctx, bot) # get repo name

    if not bot.repo_name: # if it is returned false, then just exit
        bot.making_issue = False # not making issue anymore
        return

    bot.issue_title = await get_issue_title(ctx, bot)

    if not bot.issue_title: # if it is returned false, then just exit
        bot.making_issue = False # not making issue anymore
        return

    bot.issue_body = await get_issue_body(ctx, bot)

    if not bot.issue_body: # if it is returned false, then just exit
        bot.making_issue = False # not making issue anymore
        return

    if not await confirmdetails(ctx, bot): # exit process if they don't confirm
        bot.making_issue = False
        return

    # they've confirmed the thing, so let's continue

    made_issue_link = await createissue(ctx, bot)
    if not made_issue_link: # if it errored out and returned false
        await ctx.send("Cancelling process, please try again", delete_after=bot.delete_delay)
        bot.making_issue = False
        return

    await ctx.send(f'All done! The issue was succesfully made! \nLink: {made_issue_link}', delete_after=bot.delete_delay)

    # set it to false, done making issue
    bot.making_issue = False

@bot.command()
async def help(ctx): # help message on ".git help"
    help_msg = """\
**TurtleCoin GitHub Bot**
Commands:
```
.git help:      Show this message
.git makeissue: Make an issue
.git cancel:    Cancel any issue being made
.git status:    View status of current issue being made
```"""
    await ctx.send(help_msg, delete_after=bot.delete_delay)

@bot.command()
async def cancel(ctx): # let user know the process is being cancelled; real thing is done seperately
    # only say this if an issue is being made and if the author is op of the issue
    if not bot.making_issue:
        await ctx.send("Nothing to cancel", delete_after=bot.delete_delay)
        return
    if bot.issue_maker_author != ctx.author.id:
        await ctx.send("You can't cancel someone else's issue!", delete_after=bot.delete_delay)
        return
    await ctx.send("Cancelled process!", delete_after=bot.delete_delay)

@bot.command()
async def status(ctx):
    status_msg = f"""\
**TurtleCoin Github Bot**
*Status*
__Currently making issue__: {bot.making_issue}
__Author__: {bot.full_username}
__Repo name__: {bot.repo_name}
__Issue title__: {bot.issue_title}
__Issue description__: {bot.issue_body}
    """
    await ctx.send(status_msg, delete_after=bot.delete_delay)

@bot.command()
async def ev(ctx, arg): # print out value of given var
    if ctx.author.id != 235707623985512451: # only i (sajo8) can use it
        await ctx.send('Sorry, only the owner of the bot can use this command!', delete_after=bot.delete_delay)
        return
    try: # check globals
        await ctx.send(globals()[arg], delete_after=bot.delete_delay)
    except KeyError: # not in globals
        # assume it's a botvar and try to send that
        args = arg.split('.')
        v = vars(bot)
        ar = args[1]
        await ctx.send(f'{arg}: {v[ar]}', delete_after=bot.delete_delay)
    except Exception as e: # catch all
        await ctx.send(f'Some error occured: {e}', delete_after=bot.delete_delay)

bot.run(token, bot=True)