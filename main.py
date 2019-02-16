from github import Github
import discord

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

original_message = None

repo_name = None
issue_title = None
issue_body = None

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
# prevent the thing from restarting every time it checks for user input
# use it and make the issue
# report back
# proper err msgs


class MyClient(discord.Client):
    global repo_name, issue_title, issue_body
    
    channel = None

    try:

        async def makeIssue(self):
            global making_issue
            making_issue = True

            def pred(m):
                global original_message
                return m.channel == original_message.channel and m.author == original_message.author
            
            try:

                if not repo_name:

                    await channel.send("It seems you'd like to make an issue! Let's continue. Type '!git cancel' at any time to cancel the process.")
                    await channel.send("**Please enter the name of the repository to which you'd like to submit an issue!** \n**Eg: !git turtlecoin-wallet-electron**")
                    repo_name = await client.wait_for('message', check=pred, timeout=30.0)    
                    repo_name = repo_name.content[4:]
                
                if not issue_title:

                    await channel.send("**Please enter the title of the issue** \n**Eg: !git Issue with sending transaction**")
                    issue_title = await client.wait_for('message', check=pred, timeout=30.0)
                    issue_title = issue_title.content[4:]
                
                if not issue_body:
                    await channel.send("\n**Please enter any extra info in the body of the issue! Optional, but recommended!**\n**Eg: !git Descriptive information on the issue** \n**Press enter to skip this step**\n")
                    issue_body = await client.wait_for('message', check=pred, timeout=30.0)
                    issue_body = issue_body.content[4:]
            
            except Exception as e:
                print(e)
                if e == 'asyncio.TimeoutError':
                    await channels.send("Timed out. Cancelling.")
                await channel.send('Some error')


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
            return

        async def what_to_do(self, message):
            global making_issue

            if not making_issue:
                try:
                    thing_to_do = message[1:]
                    print(thing_to_do)
                    if thing_to_do[0] == 'makeissue':
                        await channel.send("We're making an issue")
                        await self.makeIssue()
                    else:
                        await channel.send('Not sure what to do, aborting')
                        return
                except Exception as e:
                    print(e)
                    return
            else: # making an issue
                try:
                    thing_to_do = message[1]
                    print(thing_to_do)
                    if thing_to_do[0] == 'makeissue':
                        await channel.send("Already making issue, use '!git cancel' to cancel current process")
                        return
                    elif thing_to_do[0] == 'cancel':
                        await channel.send('Cancelling...')
                        making_issue = False
                        return
                    else:
                        print("doing something else, passsing it again")
                        await self.makeIssue()
                except Exception as e:
                    print(e)
        
        async def getInput(self, message):        
            inputed = message.split(" ")

            if inputed[0] != "!git": # Not directed to bot, discard it
                await channel.send("Not what we want, ignoring")
                return
            else:
                await self.what_to_do(message=inputed) # Sent to the bot, pass it off to a function

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
            global original_message

            # if the bot sent the message ignore it
            if message.author == client.user:
                return
            # someone else said it, print its content
            print(message.content)

            original_message = message
            
            await self.getInput(message=message.content)

    except KeyboardInterrupt:
        print('\nExiting.. see you!\n')

# connect to discord
client = MyClient()
client.run(token)