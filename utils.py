import globals

def get_current_issue(ctx):
    """
    Loops through list of currents issue and checks if 
    the author passed is already making an issue.
    If so, it returns the issue.
    Otherwise, it returns False
    """

    author_id = ctx.author.id
    for issue in globals.issue_queue:
        existing_issue_author_id = issue.get_author_id()
        if existing_issue_author_id == author_id:
            return issue
    return False

def get_current_issue_author_id(ctx):
    issue = get_current_issue(ctx)
    author_id = issue.get_author_id()
    return author_id

def author_is_making_issue(ctx):
    current_author_making_issue = get_current_issue(ctx)
    if current_author_making_issue:
        return True
    else:
        return False

def cancel_current_issue(ctx):
    """
    Cancel current issue
    Determined by author of the message
    Returns True if successfully cancelled
    Returns False otherwise
    """
    issue = get_current_issue(ctx)
    if issue:
        globals.issue_queue.remove(issue)
        return True
    return False

def making_issue_status():
    if len(globals.issue_queue) > 0:
        return True
    else:
        return False

def check_message(ctx, m):
    """
    Used to validate user response for multiple criteria

    - original channel and original author
    - msg starts with ".git"
    - msg not in reserved commands
    - msg is not an evalute command

    If it matches all of these, then it is a valid response
    Otherwise, it's wrong
    """

    return m.channel == ctx.channel and m.author == ctx.author and m.content.startswith(".git") and m.content[5:] not in globals.reserved_commands and m.content[5:7] not in globals.reserved_commands


    

##############

from threading import Thread
from time import sleep

# Timer which keeps getting repo names
# Runs once, then repeats once every day
# Runs on a separate thread and doesn't interfere

class BackgroundTimer(Thread):
    def __init__(self, github_org):
        super(BackgroundTimer, self).__init__() # calls the __init__() function
        self.github_org = github_org

    def get_org_repos(self):
        globals.github_org_repos = self.github_org.get_repos()

    def run(self):
        while True:
            self.get_org_repos()
            sleep(86400) # sleep for one day

##############