from github import Github
#import asyncio

# no need to try since we know it exists
username = 'Soja8'
password = open('password.txt').read()

g = Github(username, password) # log into github my g

async def createissue(ctx, bot):

    await ctx.send("Making issue...")
    
    if bot.__TEST_MODE:
        github_repo = g.get_repo("Soja8/test")
    else:
        github_repo = g.get_repo(f"TurtleCoin/{bot.repo_name}")
    
    try:
        made_github_issue = github_repo.create_issue(title=bot.issue_title, body=bot.issue_body)
    except Exception as e:
        await ctx.send("Error! {e}".format(e))
        return False
    
    github_issue_number = made_github_issue.number
    
    if bot.__TEST_MODE:
        github_issue_link = f"https://github.com/soja8/test/issues/{github_issue_number}"
    else:
        github_issue_link = f"https://github.com/TurtleCoin/{bot.repo_name}/issues/{github_issue_number}"
    
    return github_issue_link
