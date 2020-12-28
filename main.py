#Thanks to pythonforengineers for this code.

import praw
import pdb
import re
import os
import time

#Bot's ending
replyEnd = "\n-----\n\nI am a bot, and this comment was posted automatically.  \nThis bot is Work in progress.  \n[The bot is open source](https://github.com/hackerncoder/AutoRepliesBot) (Come help me out)."

#Create reddit bot instance
reddit = praw.Reddit('autoBot')

#Load in all replied to posts, not efficent my ass, make it better if you cant live with it. 
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))
        
#Point the bot at r/TOR
subreddit = reddit.subreddit('tor')

#Read the 5 newest posts (luckily r/TOR isnt that active)
while True: 
    for submission in subreddit.new(limit=5):
    
        #Check to ensure we don't spam a post
        if submission.id not in posts_replied_to:
        
            if submission.link_flair_text == "FAQ":

                if re.search("vpn", submission.selftext, re.IGNORECASE):
                        #RE is regex, anyone that knows regex please help create a string that correctly identifies posts.

                    #Check for markers for anti-vpn (don't want to add a comment saying VPN bad to someone saying they aren't using vpn).
                    #"Recommend(ed)" Is not fun to do, you could phrase it in so many ways. Check the added txt file - HkrNCdr
                    if not re.search("don(\')*t use( a)* vpn|\
                        didn(\')*t use( a)* vpn|\
                        should(n(\')*t| not) (be )*us(e|ing) (a )*vpn|\
                        not using( a)* vpn|\
                        will not( be)* us(e|ing)( a)* vpn|\
                        orbot vpn", submission.selftext, re.IGNORECASE):
            
                        #Put everything in a file to make this code just a little more readable.
                        with open("vpnReply.txt", "r") as f:
                    
                            #Now reply
                            submission.reply(f.read() + replyEnd)

                            print("Bot replying to: ", submission.title)

                        #Add the post to our list
                        posts_replied_to.append(submission.id)
                    
    for mention in reddit.inbox.mentions(limit=10):
        if not mention.submission.id in posts_replied_to:
            if re.search("u\/AutoRepliesBot.{0,4}(mobile|android|ios)", mention.body, re.IGNORECASE):
                with open("mobileReply.txt", "r") as f:
                    mention.reply(f.read() + replyEnd)
            elif re.search("u\/AutoRepliesBot.{0,4}letterboxing", mention.body, re.IGNORECASE):
                with open("letterboxingReply.txt", "r") as f:
                    mention.reply(f.read() + replyEnd)
            else:
                with open("vpnReply.txt", "r") as f:
                    mention.reply(f.read() + replyEnd)
            posts_replied_to.append(mention.submission.id)

    #Overwrite the posts_replied_to.txt with current list
    with open("posts_replied_to.txt", "w") as f:
        for posts_id in posts_replied_to:
            f.write(posts_id + "\n")

    time.sleep(120)
