import asyncio

async def check_if_repo_exists(repo_name, ctx, bot):
    await ctx.send("Checking...")
    # check if repo_name is in the list of repos
    # if it is, then it's valid, otherwise it aint
    for repo in bot.github_org_repos:
        github_repo_name = repo.name
        if repo_name == github_repo_name: # valid repo
            return True
    return False # invalid repo

async def get_repo_name(ctx, bot):

    def check(m):
        # the original channel and the orignial author
        # if the msg starts with ".git"
        # if the msg is NOT in the reserved_commands
        # if the msg is not for evaluating something (.git ev sometihng)
        return m.channel == ctx.channel and m.author == ctx.author and m.content.startswith(".git") and m.content[5:] not in bot.reserved_commands and m.content[5:7] not in bot.reserved_commands
        # if all of these are true, it's a valid repo_name
        # otherwise it isn't; ignore it and keep waiting for something
        # we wait till a) we get a valid name or b) we timeout (1 minute+)
    
    await ctx.send("**Please enter the name of the repository in which you'd like to make an issue!** \n*Eg: `.git turtlecoin-docs`*")

    try:
        # wait for message
        repo_name = await bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError: 
        # cancel the process if the guy takes more than a minute
        await ctx.send("*You took too long!* **Cancelling process.**")
        return False
    
    repo_name = repo_name.content[5:] # strip the .git part

    if repo_name == 'cancel': # if it's a cancel then exit out
        return False
    
    if bot.__TEST_MODE: # return it w/out checking since just testing
        return repo_name
    
    repo_exists = await check_if_repo_exists(repo_name, ctx, bot)
    
    if repo_exists: # it's all good
        await ctx.send("**Valid repo name!** Let's continue")
        return repo_name
    else: # invalid, retart
        await ctx.send("**Invalid repo name!** Please try again")
        await get_repo_name(ctx, bot) # restart 
