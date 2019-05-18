import asyncio

async def confirmdetails(ctx, bot):

    accepted_commands = ["cancel", "continue"]

    def check(m):
        # the original channel and the orignial author
        # if the msg starts with ".git"
        # if the msg is NOT in the reserved_commands
        # if the msg is not for evaluating something (.git ev sometihng)
        return m.channel == ctx.channel and m.author == ctx.author and m.content.startswith(".git") and m.content[5:] not in bot.reserved_commands and m.content[5:7] not in bot.reserved_commands and m.content[5:] in accepted_commands
        # if all of these are true, it's a valid repo_name
        # otherwise it isn't; ignore it and keep waiting for something
        # we wait till a) we get a valid name or b) we timeout (1 minute+)
    
    await ctx.send(f'**Chosen information:**\n*Type `.git continue` to make the issue or `.git cancel` to cancel the process.*\n**Repo name:** {bot.repo_name}\n**Issue title:** {bot.issue_title}\n**Issue body:** {bot.issue_body}')

    try:
        # wait for message
        continue_confirmation = await bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        # cancel process if the guy takes more than a minute
        await ctx.send("*You took too long!* **Cancelling process.**")
        return False
    
    continue_confirmation = continue_confirmation.content[5:] # strip git
    
    if continue_confirmation == 'cancel': # cancel process
        return False
    else:
        return True