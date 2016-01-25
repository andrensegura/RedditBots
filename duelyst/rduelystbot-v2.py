#! /usr/bin/python

import praw
import re
from time import sleep
from lxml import html, etree
import requests

import logging
logging.basicConfig(level=logging.CRITICAL, filename="rdwb.log", filemode="a+",
                        format="%(message)s")

def get_card_info(card):
    card_info = ["", "", ""]

    card_title = card.title() if card.lower() != "mechaz0r!" else "MECHAZ0R!"

    wiki_link = "http://duelyst.gamepedia.com/File:%s.png" % ('_'.join(card_title.split()) )
    db_link = "http://duelystdb.com/card/%s" % ('_'.join(card_title.split()) )

    page = requests.get(wiki_link)
    tree = html.fromstring(page.content)
    picture = tree.xpath('//div[@class="fullImageLink"]/a')

    page = requests.get(db_link)
    tree = html.fromstring(page.content)
    quick_facts = tree.xpath('//div[@class="quick_facts_inner"]/ul/li')
    stats = tree.xpath("""//div[@class="col_right"]/div/div/div[@class="duelystdb_mana_cost"]/text()
                       | //div[@class="col_right"]/div/div/div[@class="duelystdb_atk"]/text()
                       | //div[@class="col_right"]/div/div/div[@class="duelystdb_hp"]/text()
                       | //div[@class="col_right"]/div/div/div[@class="duelystdb_type"]/text() """)
    card_text = tree.xpath(""" //div[@class="col_right"]/div/div/div[@class="duelystdb_text"]/span/b/text()
                       | //div[@class="col_right"]/div/div/div[@class="duelystdb_text"]/span/text() """)

    try:
        card_info[0] = picture[0].attrib['href']
    except:
        card_info[0] = ""

    try:
        card_info[1] = stats

        tmp = []
        for elem in card_text:
            if '\\n' in elem:
                continue
            tmp.append(elem.strip())
        tmp = ' '.join(tmp)
        card_info[1].append(tmp)

    except:
        card_info[1] = ""

    try:
        tmp = []
        for elem in quick_facts:
            elem = elem.text_content().split()
            elem[0] = "**%s**" % (elem[0])
            tmp.append(' '.join(elem) )
        tmp.pop()
        card_info[2] = tmp 
    except:
        card_info[2] = ""

    return card_info
    

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

try:
    replied_to = [line.rstrip('\n') for line in open('rdwb.log')]
    print "Log file opened successfully."

except:
    print "Couldn't open log file!"
    import sys
    sys.exit()

while True:

    duelyst_comments = duelyst_sub.get_comments()
    flat_comments = praw.helpers.flatten_tree(duelyst_comments)

    for comment in flat_comments:
        try:
            if comment.id not in replied_to: 
                cards = []
                for card in re.findall(r'\{\{(.*?)\}\}', comment.body):
                    cards.append(card.lower())
                for card in re.findall(r'\[\[(.*?)\]\]', comment.body):
                    cards.append(card.lower())
                cards = list(set(cards))
                if cards:
                    reply = ""
                    print "Card found: %s" % (cards)
                    for card in cards:
                        card_info = get_card_info(card)
                        print card_info
                        if card_info and card_info[0] != "":
                            reply += "[%s](%s)\n\n" % (card.title(), card_info[0])
                            reply += ">**Stats:** %s/%s/%s **Type:** %s\n\n" % (card_info[1][0],
                                    card_info[1][2], card_info[1][3], card_info[1][1])
                            reply += ">**Text:** %s\n\n>" % (card_info[1][4])

                            for stat in card_info[2]:
                                reply += "%s " % (stat)
                            reply += "\n\n"
                        else:
                            pass
                    if reply:
                        reply += "\n\n---------\n\n ^Bugs, ^requests, ^questions? ^PM ^/u/bibbleskit!"
                    else:
                        reply += "Sorry, none of those cards came up! Perhaps you made some typos."
                        reply += "\n\n---------\n\n ^Bugs, ^requests, ^questions? ^PM ^/u/bibbleskit!"
                    try:
                        comment.reply(reply)
                        replied_to.append(comment.id)
                        logging.critical("%s" % (comment.id) )
                    except Exception,e: print "1 " + str(e)
                else:
                   pass 
        except Exception,e: print "2: " + str(e) 
    print "Sleeping for 120 seconds..."
    sleep(60)
    print "60 seconds to go..."
    sleep(60)
    print "Checking new comments!"

