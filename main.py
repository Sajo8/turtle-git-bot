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
    pass

g = Github(username, password)

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

class MyClient(discord.Client):
    channel = None

    async def makeIssue(self, thing_to_do):
        await channel.send("\nIt seems you'd like to make an issue! Let's continue. Type '!git cancel' at any time to cancel the process.")
        try:

            if thing_to_do == 'cancel':
                await channel.send('Cancelling..')
                return
            
            issue_repo = input("\n**Please enter the name of the repository to which you'd like to submit an issue!** \n**Eg: turtlecoin-wallet-electron**\n")
            issue_title = input("\n**Please enter the title of the issue**\n")
            issue_body = input("\n**Please enter any extra info in the body of the issue! Optional, but recommended!**\n**Press enter to skip this step**\n")

            print('\nMaking issue...')

            try:
                repo = g.get_repo(f'Soja8/{issue_repo}')
            except:
                print("Some error occured, please try again!")
                return

            repo.create_issue(title=issue_title, body=issue_body)

            print('\nAll done! The issue was succesfully made!')

        except KeyboardInterrupt:
            print('\nQuitting... \nSee you!')
            return

    async def what_to_do(self, given_input):

        thing_to_do = given_input[1]

        if thing_to_do == 'makeissue':
            await channel.send("We're making an issue")
            await self.makeIssue(thing_to_do)
        else:
            await channel.send('Not sure what to do, aborting')
            return
    
    async def getInput(self, message):
    
        inputed = message.split(" ")

        if inputed[0] != "!git": # not what we want
            await channel.send("Not what we want, ignoring")
            return
        else:
            await self.what_to_do(given_input=inputed) # what we want, pass it off to a function

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
        # if the bot sent the message ignore it
        if message.author == client.user:
            return
        # someone else said it, print its content
        print(message.content)
        await self.getInput(message=message.content)

# connect to discord
client = MyClient()
client.run(token)