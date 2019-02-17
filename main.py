from github import Github
import discord
import traceback

username = 'Soja8'

try:
    password = open('password.txt').read()
except:
    print("Can't find password file, aborting.")
    exit()

try:
    token = open('tokenfile.txt').read()
except:
    print("Can't find token file, aborting.")
    exit()

g = Github(username, password)
making_issue = False

repo_name = False
issue_title = False
issue_body = False

original_message = None

# Get input
# If it starts with !git then continue, else forget about it

# Check the next two:
# what to deal with and
# what to do with thing
# for eg:
# issue, make
# deal with issues; we have to make one

# then based on the scenario take input
# in this case
# repo to submit issue to

# this warrants a list of repos

# and the title
# body is optional

# if they just do "!git issue make" then walk them through
# or make it only walk-through able
# like in the wallets

# def getInput()
# def what_to_do()
# def makeIssue()
# 

#########################################################################################################################

# make it continous like in trtl cli py
# make it check only the same channel for 30s - 1m for a response from the same user who iniated the thing
# then use it

# catch errors
# return a descriptive one

# pass the content of the message to makeIssue() so that it can get the details
# make sure cancelling thing works

# prevent exiting and re-logging in of bot when error making issue

# TODO
# wait for user to enter something
# still check incoming msgs
# prevent the thing from discaring the name of the thing...??????
# use it and make the issue
# report back
# proper err msgs


class MyClient(discord.Client):

    channel = None

    try:

        async def makeIssue(self, info=None):
            global making_issue, repo_name, issue_title, issue_body
            making_issue = True

            def check(m):
                global original_message
                return m.channel == original_message.channel and m.author == original_message.author

            if not repo_name:
                if not info:
                    await channel.send("It seems you'd like to make an issue! Let's continue. Type '!git cancel' at any time to cancel the process.")
                    await channel.send("**Please enter the name of the repository to which you'd like to submit an issue!** \n*Eg: !git turtlecoin-wallet-electron*")
                    repo_name = await client.wait_for('message', check=check, timeout=30.0)
                else:
                    try:
                        repo_name = await client.wait_for('message', check=check, timeout=30.0)
                        print(repo_name)
                        repo_name = repo_name.content[4:]
                        #info = None
                        return
                    except:
                        print("whoops")
                        traceback.print_exc()
            
            if not issue_title:
                if not info:
                    await channel.send("**Please enter the title of the issue** \n*Eg: !git Issue with sending transaction*")
                    issue_title = await client.wait_for('message', check=check, timeout=30.0)
                else:
                    try:
                        issue_title = await client.wait_for('message', check=check, timeout=30.0)
                        print(issue_title)
                        issue_title = issue_title.content[4:]
                        #info = None
                        return
                    except:
                        print("whoops2")
                        traceback.print_exc()
            
            if not issue_body:
                if not info:
                    await channel.send("\n**Please enter any extra info in the body of the issue! Optional, but recommended!**\n*Eg: !git Descriptive information on the issue* \n*Type `!git` to skip this step*\n")
                    issue_body = await client.wait_for('message', check=check, timeout=30.0)
                else:
                    try:
                        issue_body = await client.wait_for('message', check=check, timeout=30.0)
                        print(issue_body)
                        issue_body = issue_body.content[4:]
                        #info = None
                        return
                    except:
                        print("whoops3")
                        traceback.print_exc()
                    
            """
            
            except Exception as e:
                traceback.print_exc()
                if e == 'asyncio.TimeoutError':
                    await channel.send("Timed out. Cancelling.")
                await channel.send('Some error')
            """
            
            print('\nMaking issue...')

            print(f"""\
            name: {repo_name}
            title: {issue_title}
            body: {issue_body}
            """)

            try:
            #repo = g.get_repo(f'Soja8/{issue_repo}')
            #repo.create_issue(title=issue_title, body=issue_body)
                print('\nAll done! The issue was succesfully made!')
            except:
                await channel.send("Some error occured, please try again!")
            
            making_issue = False
            return

        async def on_ready(self):
            global channel

            # let us know we're ready
            print('Logged on as {0}!'.format(self.user))

            # get channel info to send info to
            channel = client.get_channel(536397649671356418)
            # NOTE: might remove this line, make it respond in the same channel it was called. or check if it's not in any but dev_ channels

            # send for da ez confirmation
            await channel.send('yeet')

        async def on_message(self, message):
            global original_message, channel, making_issue

            # if the bot sent the message ignore it
            if message.author == client.user:
                return
            
            # someone else said it, print its content
            print(message.content)

            original_message = message

            inputed = message.content.split(" ")

            print(inputed)

            if inputed[0] != "!git":
                await channel.send("Not what we want, ignoring")
                return
            
            thing_to_do = inputed[1:]

            if not making_issue:
                try:
                    if thing_to_do[0] == 'makeissue':
                        await channel.send("We're making an issue")
                        await self.makeIssue()
                    else:
                        await channel.send('Not sure what to do, aborting')
                        return
                except:
                    traceback.print_exc()
                    return
            else: # currently in the process of making an issue
                try:
                    if thing_to_do[0] == 'makeissue':
                        await channel.send("Already making issue, use '!git cancel' to cancel current process")
                        return
                    elif thing_to_do[0] == 'cancel':
                        await channel.send('Cancelling...')
                        making_issue = False
                        return
                    else:
                        await self.makeIssue(info=thing_to_do)
                except:
                    traceback.print_exc()

            """
            elif making_issue and not issue_title:
                issue_title = await client.wait_for('message', check=check, timeout=30.0)
                issue_title = issue_title.content[4:]
                await channel.send(f"issue_title: {issue_title}")

            elif making_issue and not issue_body:
                issue_body = await client.wait_for('message', check=check, timeout=30.0)
                issue_body = issue_body.content[4:]
                await channel.send(f"issue_body: {issue_body}")
            """
            

    except KeyboardInterrupt:
        print('\nExiting.. see you!\n')

# connect to discord
client = MyClient()
client.run(token)