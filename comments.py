# TODO
# Catch errors, return descriptive ones
# Change how .git ev works


# DONE
# Make sure makeissue can't be called multiple times
# Cancel everything when .git cancel is called
# Make sure you can't do .git help or something when we're waiting for a repo name
# Do the issue title and issue body part

# for .git ev
# try to do split(.)
# then do 
# globals()[0].[1]
# that way it works with normal stuff
# and with ctx as well as bot

# Maybe make some .git status so that we can check the current status in the issue making thing: currently set repo name, issue title, issue body, etc.
# make a git req class
# assosicate makingissue with some user id


# possibly make a req class
#class github req
# properties (See below comment)
# list of these comments
# associated with author
# can make multiple at once
# would be cool beo

#------------------------------------

##############################

# Class Github request
# title
# repo
# body
# link
# success/fail
# maker id
# maker user name

# we dont need an issue class mb
# just a function, and apss this to it

# func to parse errors
# and return in a proper manner

# class issue request
# orig author
# repo, title, body
# issue_request.make_issue() which does it for me
# then stuff to get sucess/fail details from it
# and content of what the repsponse is

##############################




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
