import globals
import utils

from GitIssue import GitIssue

from github import Github
from discord.ext import commands

from reponame import get_repo_name
from issuetitle import get_issue_title
from issuebody import get_issue_body
from waitforconf import confirmdetails
from creategitissue import createissue

# try to get tokenfile and password
# we don't need the password but try anyways just to check
try:
    open('password.txt')
    _token = open('tokenfile.txt').read()
except:
    print("Can't find password/token file, aborting.")
    exit()

g = Github()
github_org = g.get_organization("TurtleCoin") # get turtlecoin org
github_org_repos = None

#####
# Start updating the repos every 24h in the background
timer = utils.BackgroundTimer(github_org)
timer.start()
#####

making_issue = False

bot = commands.Bot(command_prefix='.git ') # set prefix
bot.remove_command('help') # remove command so that we can make our own

# TurtleCoin, jc5Traq
allowed_servers = [388915017187328002]

@bot.event
async def on_ready():
    # send ready msg to personal server
    channel = bot.get_channel(591108780020727824)
    await channel.send("Github bot's up") # when ready send a confirmation message
    print("Bot up!")

@bot.event
async def on_guild_join(guild):
    if guild.id not in allowed_servers:
        guild.leave()

@bot.command()
async def makeissue(ctx): # we makin an issue bois
    global making_issue

    await ctx.message.delete(delay=globals.msg_deletion_delay)

    # save author id
    author_id = ctx.author.id
    # save author username
    author = await bot.fetch_user(author_id)
    author_username = f"@{author.name}#{author.discriminator}"

    # If someone who is already making an issue is trying to make another, then stop
    if making_issue:
        if utils.author_is_making_issue(ctx):
            await ctx.send(f"<@{author_id}>, you are already making an issue! Say `.git cancel` to cancel the current process.", delete_after=globals.msg_deletion_delay)
            return

    # Make a new issue, add it to the list, and get the latest issue just made for future reference
    new_issue = GitIssue(author_id = author_id, author_username = author_username)
    globals.issue_queue.append(new_issue)
    globals.latest_issue = globals.issue_queue.index(new_issue)

    await ctx.send(f"<@{author_id}>, it seems you'd like to make an issue! Let's continue. Say `.git cancel` at any time to cancel the process.", delete_after=globals.msg_deletion_delay)

    # update making_issue status
    making_issue = utils.making_issue_status()

    repo_name = await get_repo_name(ctx, bot) # get repo name
    utils.get_current_issue(ctx).set_repo_name(repo_name)

    if not repo_name:
        # If it returns false, then cancel current issue
        utils.cancel_current_issue(ctx)
        # Update making issue status
        making_issue = utils.making_issue_status()
        return

    issue_title = await get_issue_title(ctx, bot)
    utils.get_current_issue(ctx).set_issue_title(issue_title)

    if not issue_title:
        # If it returns false, then cancel current issue
        utils.cancel_current_issue(ctx)
        # Update making issue status
        making_issue = utils.making_issue_status()
        return

    issue_body = await get_issue_body(ctx, bot)
    utils.get_current_issue(ctx).set_issue_body(issue_body)

    if not issue_body:
        # If it returns false, then cancel current issue
        utils.cancel_current_issue(ctx)
        # Update making issue status
        making_issue = utils.making_issue_status()
        return

    if not await confirmdetails(ctx, bot): # exit process if they don't confirm
        utils.cancel_current_issue(ctx)
        making_issue = utils.making_issue_status()
        return

    # they've confirmed the thing, so let's continue

    made_issue_link = await createissue(ctx, bot)
    if not made_issue_link: # if it errored out and returned false
        await ctx.send(f"<@{author_id}>, cancelling process, please try again", delete_after=globals.msg_deletion_delay)
        utils.cancel_current_issue(ctx)
        making_issue = utils.making_issue_status()
        return

    await ctx.send(f"<@{author_id}>, all done! The issue was succesfully made! \nLink: {made_issue_link}", delete_after=globals.msg_deletion_delay)

    # Remove issue from queue and update making issue status
    # Doesn't really "cancel" it
    utils.cancel_current_issue(ctx)
    making_issue = utils.making_issue_status()

@bot.command()
async def help(ctx): # help message on ".git help"
    await ctx.message.delete(delay=globals.msg_deletion_delay)
    help_msg = f"""\
**TurtleCoin GitHub Bot**
Commands:
```
.git help:      Show this message
.git makeissue: Make an issue
.git cancel:    Cancel any issue being made
.git status:    View status of current issue being made
```
<@{ctx.author.id}>"""
    await ctx.send(help_msg, delete_after=globals.msg_deletion_delay)

@bot.command()
async def cancel(ctx): 
    global making_issue

    # let user know the process is being cancelled; real thing is done seperately
    # only say this if an issue is being made and if the author is op of the issue
    
    await ctx.message.delete(delay=globals.msg_deletion_delay)

    author_id = ctx.author.id
    
    if utils.author_is_making_issue(ctx):
        # attempt to cancel issue which the author is making

        cancelled_successfully = utils.cancel_current_issue(ctx)
        if cancelled_successfully:
            await ctx.send(f"<@{author_id}>, cancelled process!", delete_after=globals.msg_deletion_delay)
        else:
            await ctx.send(f"<@{author_id}>, sorry, something went wrong. Couldn't cancel the process.", delete_after=globals.msg_deletion_delay)
        # update making_issue status
        making_issue = utils.making_issue_status()
    else:
        # author was never making an issue
        await ctx.send(f"<@{author_id}>, you aren't making an issue currently.", delete_after=globals.msg_deletion_delay)
        return


@bot.command()
async def status(ctx):
    global making_issue
    await ctx.message.delete(delay=globals.msg_deletion_delay)

    current_issue = utils.get_current_issue(ctx)
    
    if current_issue:
        author_id = current_issue.get_author_id()
        repo_name = current_issue.get_repo_name()
        issue_title = current_issue.get_issue_title()
        issue_body = current_issue.get_issue_body()

        status_msg = f"""\
**TurtleCoin GitHub Bot**
*Status*
<@{author_id}>, here's the info in your issue currently:
__Repo name__: {repo_name}
__Issue title__: {issue_title}
__Issue description__: {issue_body}
    """

    else:
        author_id = ctx.author.id
        status_msg = f"""\
**TurtleCoin GitHub Bot**
*Status*
<@{author_id}>, you're not making an issue currently!
    """
    await ctx.send(status_msg, delete_after=globals.msg_deletion_delay)

@bot.command()
async def ev(ctx, arg): # print out value of given var
    await ctx.message.delete(delay=globals.msg_deletion_delay)
    if ctx.author.id != 235707623985512451: # only i (sajo8) can use it
        await ctx.send(f'<@{ctx.author.id}>, sorry, only the owner of the bot can use this command!', delete_after=globals.msg_deletion_delay)
        return
    if arg == "issue_queue":
        await ctx.send(globals.issue_queue, delete_after=globals.msg_deletion_delay)
    try: # check globals
        await ctx.send(globals()[arg], delete_after=globals.msg_deletion_delay)
    except KeyError: # not in globals
        # assume it's a botvar and try to send that
        args = arg.split('.')
        v = vars(bot)
        ar = args[1]
        await ctx.send(f'{arg}: {v[ar]}', delete_after=globals.msg_deletion_delay)
    except Exception as e: # catch all
        await ctx.send(f'Some error occured: {e}', delete_after=globals.msg_deletion_delay)

bot.run(_token, bot=True)