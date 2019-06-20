import asyncio

async def get_issue_body(ctx, bot):

    def check(m):
        # the original channel and the orignial author
        # if the msg starts with ".git"
        # if the msg is NOT in the reserved_commands
        # if the msg is not for evaluating something (.git ev sometihng)
        return m.channel == ctx.channel and m.author == ctx.author and m.content.startswith(".git") and m.content[5:] not in bot.reserved_commands and m.content[5:7] not in bot.reserved_commands
        # if all of these are true, it's a valid repo_name
        # otherwise it isn't; ignore it and keep waiting for something
        # we wait till a) we get a valid name or b) we timeout (1 minute+)
    
    await ctx.send("**Please enter a description of the issue you'd like to make!** \n*Eg: `.git (Descriptive information on the issue here)`*", delete_after=bot.msg_wait_and_delete_delay)

    try:
        # wait for message
        issue_body = await bot.wait_for('message', check=check, timeout=bot.msg_wait_and_delete_delay)
        await issue_body.delete(delay=bot.msg_wait_and_delete_delay)
    except asyncio.TimeoutError:
        # cancel process if the guy takes more than a minute
        await ctx.send("*You took too long!* **Cancelling process.**", delete_after=bot.msg_wait_and_delete_delay)
        return False
    
    issue_body = issue_body.content[5:] # strip the ".git "

    if issue_body == 'cancel': # exit out if it's cancel
        return False

    await ctx.send("**Received issue description!** Let's continue", delete_after=bot.msg_wait_and_delete_delay)

    return issue_body

    # NOTE: maybe add some more chceks??
    # like if it's not empty
    # or a word threshold
