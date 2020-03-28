import praw
import codecs;
from datetime import datetime


def utc_to_time(utc):
    return str(datetime.utcfromtimestamp(int(float(utc))))

def safeInput(thing):
    """
    removes problematic commas and newline characters from strings
    :param thing: any object that can be cast to a string
    :return: a clean string
    """
    x = str(thing).replace(",", "")
    x = x.replace("\n", "")
    return x

def subreddits_to_csv():
    reddit = praw.Reddit('bot1')
    file = codecs.open("saved_subreddits.csv", "w", "utf-8")
    print()
    count = 0
    file.write("Subreddit , link\n")
    # Gets the saved paginator
    subscribed_subreddits = list(reddit.user.subreddits(limit=None))
    for entry in subscribed_subreddits:
        file.write(entry.display_name + ", https://www.reddit.com/r/" + entry.display_name + "\n")
    file.close()

   

def saved_to_csv():
    """
    the main bot code, goes through saved posts and comments, saving them in CSV format
    :return: nothing
    """
    reddit = praw.Reddit('bot1')
    file = codecs.open("savedSaved.csv", "w", "utf-8")
    print()
    count = 0
    file.write("Type , Subreddit , Author, PermaLink, Time, Title, body\n")
    #Gets the saved paginator
    SavedListing = reddit.get("user/UserName/saved", {'limit': 100})
    savedString = SavedListing.after
    while(True):
        #gets saved posts from paginator
        page = SavedListing.children
        for entry in page:
            try:
                toWrite = ""
                if(type(entry) is praw.reddit.Submission):
                    #format for a submission. Comments lack titles, and submission body is called self text
                    toWrite += "Submission , " + safeInput(entry.subreddit.display_name) + " , " + safeInput(entry.author.name) +" , " + safeInput(entry.permalink)+ " , " + safeInput(utc_to_time(str(entry.created_utc)))  + " , " +safeInput(entry.title) +" , "
                    if(entry.selftext != ""):
                        #if self text exists, write it
                        toWrite += safeInput(entry.selftext)
                elif(type(entry) is praw.reddit.Comment):
                    #Same thing but if is of type comment
                    toWrite += "Comment , " + safeInput(entry.subreddit.display_name) + " , " + safeInput(entry.author.name) + " , " + safeInput(entry.permalink) + " ,"  + safeInput(utc_to_time(str(entry.created_utc)))  + " ,, " + safeInput(entry.body)
                file.write(toWrite + "\n")
                toWrite = ""
            except:
                print(Exception.__name__)
                toWrite = ""
                #Sometimes things get deleted, so I through these entries away\
        #gets the next page from the paginator, breaks out if there is no next page
        SavedListing = reddit.get("user/User/saved", {'limit': 100, 'after' : savedString})
        savedString = SavedListing.after
        if(savedString is None):
            file.close()
            exit()




