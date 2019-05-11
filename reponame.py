import asyncio

async def check_if_repo_valid(repo_name, ctx, bot):
    await ctx.send("Checking...")
    # if the repo_name is in the list of repos, then it's True. otherwise it's not
    for repo in bot.github_org_repos:
        github_repo_name = repo.name
        if repo_name == github_repo_name:
            return True
    return False

async def get_repo_name(ctx, bot):

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author and m.content.startswith(".git")
    
    await ctx.send("**Please enter the name of the repository in which you'd like to make an issue!** \n*Eg: `.git turtlecoin-wallet-electron`*")

    try:
        repo_name = await bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError: # cancel the process if the guy takes more than a minute
        await ctx.send("*You took too long!* **Cancelling process.**")
        return False
    repo_name = repo_name.content[5:]

    if bot.__TEST_MODE: # return it w/out checking since just testing
        return repo_name
    
    if await check_if_repo_valid(repo_name, ctx, bot): # it's all good
        await ctx.send("**Valid repo name!** Let's continue")
        return repo_name
    else: # invalid, return false and quit
        await ctx.send("**Invalid repo name!** Please try again")
        await get_repo_name(ctx, bot) # restart
