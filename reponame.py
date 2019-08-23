import asyncio
import utils
import globals

async def check_if_repo_exists(repo_name, ctx):
    await ctx.send(f"<@{ctx.author.id}, validating repo...", delete_after=globals.msg_deletion_delay)
    # check if repo_name is in the list of repos
    # if it is, then it's valid, otherwise it aint
    for repo in globals.github_org_repos:
        github_repo_name = repo.name
        if repo_name == github_repo_name: # valid repo
            return True
    return False # invalid repo

async def get_repo_name(ctx, bot):

    author_id = utils.get_current_issue_author_id(ctx)

    def check(m):
        
        msg_valid = utils.check_message(ctx, m)
        return msg_valid

        # If this returns true, it's valid
        # Otherwise, we ignore it and keep waiting
        # Either till we get a valid name or the timeout

    await ctx.send(f"<@{author_id}>, **please enter the name of the repository in which you'd like to make an issue!** \n*Eg: `.git turtlecoin-docs`*", delete_after=globals.msg_deletion_delay)

    try:
        # wait for message
        repo_name = await bot.wait_for('message', check=check, timeout=globals.msg_deletion_delay)
        await repo_name.delete(delay=globals.msg_deletion_delay)
    except asyncio.TimeoutError: 
        # cancel the process if the guy takes more than the set timeout
        await ctx.send(f"<@{author_id}>, *you took too long!* **Cancelling process.**", delete_after=globals.msg_deletion_delay)
        return False
    
    repo_name = repo_name.content[5:] # strip the .git part

    if repo_name == 'cancel': # if it's a cancel then exit out
        return False
    
    if globals.test_mode: # return it w/out checking since just testing
        return repo_name
    
    repo_exists = await check_if_repo_exists(repo_name, ctx)
    
    if repo_exists: # it's all good
        await ctx.send(f"<@{author_id}>, **valid repo name!** Let's continue", delete_after=globals.msg_deletion_delay)
        return repo_name
    else: # invalid, retart
        await ctx.send(f"<@{author_id}>, **invalid repo name!** Please try again", delete_after=globals.msg_deletion_delay)
        await get_repo_name(ctx, bot) # restart 
