global issue_queue
issue_queue = [] # list of all issues being made

global test_mode
test_mode = False # used to bypass any checks and make issue in test repo

global reserved_commands
reserved_commands = ['help', 'makeissue', 'ev', 'status'] # commands which do not count as repo_names or stuff like that
# cancel is not included since we need to check that seperately

global msg_deletion_delay
msg_deletion_delay = 300.0 # time after which a message is auto deleteed
# 5 minutes

global github_org_repos
github_org_repos = None

global latest_issue
latest_issue = None