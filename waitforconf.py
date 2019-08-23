import asyncio
import utils
import globals

async def confirmdetails(ctx, bot):

    accepted_commands = ["cancel", "continue"]
    author_id = utils.get_current_issue_author_id(ctx)

    def check(m):

        msg_valid = utils.check_message(ctx, m)
        if msg_valid:
            # Do one more check, should only be two options
            # "cancel" or "continue"
            msg_valid = m.content[5:] in accepted_commands
        return msg_valid
        
        # If this returns true, it's valid
        # Otherwise, we ignore it and keep waiting
        # Either till we get a valid name or the timeout
    
    current_issue = utils.get_current_issue(ctx)

    repo_name = current_issue.get_repo_name()
    issue_title = current_issue.get_issue_title()
    issue_body = current_issue.get_issue_body()
    
    await ctx.send(f"<@{author_id}>, **Chosen information:**\n*Type `.git continue` to make the issue or `.git cancel` to cancel the process.*\n**Repo name:** {repo_name}\n**Issue title:** {issue_title}\n**Issue body:** {issue_body}", delete_after=globals.msg_deletion_delay)

    try:
        # wait for message
        continue_confirmation = await bot.wait_for('message', check=check, timeout=globals.msg_deletion_delay)
        # delete confirmation message
        await continue_confirmation.delete(delay=globals.msg_deletion_delay)
    except asyncio.TimeoutError:
        # cancel process if the guy takes more than a minute
        await ctx.send(f"<@{author_id}>, *you took too long!* **Cancelling process.**", delete_after=globals.msg_deletion_delay)
        return False
    
    continue_confirmation = continue_confirmation.content[5:] # strip git
    
    if continue_confirmation == 'cancel': # cancel process
        return False
    else:
        return True