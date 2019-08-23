class GitIssue:
    
    def __init__(self, repo_name = None, issue_title = None, issue_body = None, author_id = None, author_username = None):
        self.repo_name = repo_name
        self.issue_title = issue_title
        self.issue_body = issue_body
        self.author_id = author_id
        self.author_username = author_username

    def get_repo_name(self):
        return self.repo_name

    def set_repo_name(self, repo_name):
        self.repo_name = repo_name
    
    def get_issue_title(self):
        return self.issue_title
    
    def set_issue_title(self, issue_title):
        self.issue_title = issue_title
    
    def get_issue_body(self):
        return self.issue_body
    
    def set_issue_body(self, issue_body):
        self.issue_body = issue_body
    
    def get_author_id(self):
        return self.author_id
    
    def get_author_username(self):
        return self.author_username
