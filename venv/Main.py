import os;
import bot;


if __name__ == "__main__":
    #Be sure to create your own praw.ini file prior to running!
    bot.saved_to_csv()
    bot.subreddits_to_csv()
    print("done")
    