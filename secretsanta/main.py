import praw
import json

##############
## Setup and Variables
##############
moderators = ['test', 'foo'] # ['bibbleskit', 'bolilo', 'pseudogenesis']
#connects to Reddit and identifies the script.
#reddit requires that you identify the bot with a meaningful statement.
r = praw.Reddit(user_agent="Secret Santa helper for /r/TsumTsum by /u/bibbleskit")

#log in
r.login('Royal_Deliverer', '********', disable_warning=True)

#make user data accessible to the bot
#entries.json contains information for each user. entries variable will be a dictionary
#example: giftee = entries['bibbleskit'] ; print(giftee['Delivery Address']) //prints "123 Street St...etc"
user_data_json_file = "entries.json"
with open(user_data_json_file) as json_file:
    entries = json.load(json_file)
#matchups.json contains information about santas/giftees. santas will be a list.
#example: print(santas[0]['Giftee']) //prints "firstRedditUsername"
matches_json_file = "matchups.json"
with open(matches_json_file) as json_file:
    santas = json.load(json_file)
    santas = santas['Match-Ups']

##############
## Relay to Giftee/Sender.
##############
#relayMessage takes two strings
#message body is what the recipient will receive
#author is from whom the message was sent
#sog is short for "santa or giftee". Should equal either 'santa' or 'giftee',
#the command that was issued.
def relayMessage(message_body, author, sog):
    #if someone is sending to their giftee, it needs to tell
    #the recipient it came from their santa (and vice versa)
    #we can also grab the recipient's username here.
    if sog == "giftee":
        sog = "santa"
        for santa in santas:
            if santa['Santa'] == author:
                recipient = santa['Giftee']
    elif sog == "santa":
        sog = "giftee"
        for santa in santas:
            if santa['Giftee'] == author:
                recipient = santa['Santa']
                break
        
    
    subject = "Message from your " + sog.capitalize()
    r.send_message(recipient, subject, message_body)
    print("message sent to " + recipient)

##############
## Create posts at scheduled times.
##############

##############
## Contact Santas with Giftee information.
##############

##############
## Manipulate Database
##############

##############
## Send Santas reminders
##############

##############
## Notify Giftee when Santa has been sent.
##############

##############
## Help information
##############
#sendHelp sends a list of available commands, not the police.
def sendHelp(recipient):
    subject = "Help Information"
    body = """To issue a command, enter one of the following in the subject (without the quotes):

- 'help' : show this message
- 'giftee' : send a message to your giftee
- 'santa' : send a message to your santa
"""
    r.send_message(recipient, subject, body)

##############
## Invalid command
##############
#invalidCommand sends a message to the command issuer letting them know
#there was an problem executing the command.
def invalidCommand(command, recipient):
    subject = "Invalid command: '" + command + "'"
    body = "The command you issued was invalid. If you need a list of commands, send a message with the subject \"help\"."
    r.send_message(recipient, subject, body)
    return

##############
## Interpret Commands
##############
#the command you want to send should be the subject of the message.

def interpretCommand(message, author):
    command = message.subject.lower()

    if (command == "giftee") or (command == "santa"):
        relayMessage(message.body, author, command)
    elif command == "help":
        sendHelp(author)
    else:
        invalidCommand(command, author)
    
def interpretModCommand(message):
    command = message.subject.lower()
    return

##############
## MAIN
##############
#interpretCommand("giftee: gotcha bitch", 'bibbleskit')
#interpretModCommand("test")
mail = r.get_unread()
for message in mail:
    #print (vars(message)) #shows all variables for this object. very useful
    #we convert it to a str because it's an "author" object or something. idr
    author = str(message.author)
    if author not in moderators:
       interpretCommand(message, author)
    else:
        interpretModCommand(message, author)
    message.mark_as_read()