from github import Github
from github.GithubException import GithubException

import utils
import globals

async def createissue(ctx, bot):

    # no need to try since we know it exists
    username = 'TurtleDiscordIssueBOT'
    password = open('password.txt').read()

    g = Github(username, password) # log into github my g

    author_id = utils.get_current_issue_author_id(ctx)

    await ctx.send(f"<@{author_id}>, making your issue...", delete_after=globals.msg_deletion_delay)

    current_issue = utils.get_current_issue(ctx)

    repo_name = current_issue.get_repo_name()
    issue_title = current_issue.get_issue_title()
    issue_body = current_issue.get_issue_body()
    author_id = current_issue.get_author_id()
    author_username = current_issue.get_author_username()

    
    if globals.test_mode:
        github_repo = g.get_repo("Soja8/test")
    else:
        github_repo = g.get_repo(f"TurtleCoin/{repo_name}")

    # add author info and note to the bdoy
    new_issue_body = f"**Issue made through Discord Bot** \n\n---\n{issue_body} \n\n---\n**Author**: {author_username}\n**Id**: {author_id}"

    current_issue.set_issue_body(new_issue_body)
    issue_body = current_issue.get_issue_body()

    try:
        made_github_issue = github_repo.create_issue(title=issue_title, body=issue_body)
    except GithubException as e:
        await ctx.send(f"<@{author_id}>, an error occured! {e}".format(e.data), delete_after=globals.msg_deletion_delay)
        return False
    
    github_issue_number = made_github_issue.number
    
    if globals.test_mode:
        github_issue_link = f"https://github.com/soja8/test/issues/{github_issue_number}"
    else:
        github_issue_link = f"https://github.com/TurtleCoin/{repo_name}/issues/{github_issue_number}"
    
    return github_issue_link