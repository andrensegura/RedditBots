#! /usr/bin/python

import praw
import re
from time import sleep
from lxml import html, etree
import requests

def get_card_link(card):
    link = "http://duelyst.gamepedia.com/File:%s.png" % ('_'.join(card.title().split()) )

    page = requests.get(link)
    tree = html.fromstring(page.content)

    picture = tree.xpath('//div[@class="fullImageLink"]/a')

    try:
        return picture[0].attrib['href']
    except:
        return ""


user_agent = "/r/duelyst card reader by /u/bibbleskit"
r = praw.Reddit(user_agent=user_agent)

#log in
r.login('duelystwikibot', '***********')

duelyst_sub = r.get_subreddit('duelyst')
duelyst_comments = duelyst_sub.get_comments()
flat_comments = praw.helpers.flatten_tree(duelyst_comments)

if not flat_comments:
    print "uhhh?"


replied_to = []

while True:

    duelyst_comments = duelyst_sub.get_comments()
    flat_comments = praw.helpers.flatten_tree(duelyst_comments)

    for comment in flat_comments:
        try:
            if comment.id not in replied_to: 
                cards = re.findall(r'\{\{(.*?)\}\}', comment.body)
                if cards:
                    reply = ""
                    print "Card found: %s" % (cards)
                    for card in cards:
                        card_link = get_card_link(card)
                        if card_link:
                            reply += "[%s](%s)\n\n" % (card.title(), card_link)
                        else:
                            print "not valid card: %s" % (card)
                    if reply:
                        reply += "---------\n\n ^(Bugs, requests, questions? PM /u/bibbleskit!)"
                    else:
                        reply += "Sorry, none of those cards came up! Perhaps you made some typos."
                        reply += "---------\n\n ^(Bugs, requests, questions? PM /u/bibbleskit!)"
                    try:
                        comment.reply(reply)
                        replied_to.append(comment.id)
                        print "Replied to comment ID %s" % (comment.id)
                    except Exception,e: print str(e)
                else:
                   pass 
        except:
            pass
    print "Sleeping for 120 seconds..."
    sleep(60)
    print "60 seconds to go..."
    sleep(60)
    print "Checking new comments!"

