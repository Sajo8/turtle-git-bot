import asyncio
import utils
import globals

async def get_issue_body(ctx, bot):

    author_id = utils.get_current_issue_author_id(ctx)

    def check(m):

        msg_valid = utils.check_message(ctx, m)
        return msg_valid

        # If this returns true, it's valid
        # Otherwise, we ignore it and keep waiting
        # Either till we get a valid name or the timeout
    
    await ctx.send(f"<@{author_id}>, **please enter a description of the issue you'd like to make!** \n*Eg: `.git (Descriptive information on the issue here)`*", delete_after=globals.msg_deletion_delay)

    try:
        # wait for message
        issue_body = await bot.wait_for('message', check=check, timeout=globals.msg_deletion_delay)
        await issue_body.delete(delay=globals.msg_deletion_delay)
    except asyncio.TimeoutError:
        # cancel process if the guy takes more than the set timeout
        await ctx.send(f"<@{author_id}>, *you took too long!* **Cancelling process.**", delete_after=globals.msg_deletion_delay)
        return False
    
    issue_body = issue_body.content[5:] # strip the ".git "

    if issue_body == 'cancel': # exit out if it's cancel
        return False

    await ctx.send(f"<@{author_id}>, **received issue description!** Let's continue", delete_after=globals.msg_deletion_delay)

    return issue_body

    # NOTE: maybe add some more chceks??
    # like if it's not empty
    # or a word threshold
