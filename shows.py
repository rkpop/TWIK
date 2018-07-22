import configparser
from datetime import date, timedelta
import praw
import re

config = configparser.ConfigParser()
config.read('config.ini')
sub_link = "https://reddit.com/r/kpop"
sub_wiki = "{}/wiki/".format(sub_link)

class Show():
    def __init__(self, name, show_link, date):
        self.name = name
        self.show_link = show_link
        self.date = date
        self.url = "{}{}{}".format(sub_wiki, show_link, date)
        self.praw_url = "{}{}".format(show_link, date)
        self.discussion_url = ""
        self.winner = ""
        self.no_broadcast = False

def get_shows():
    show_links = [
        "music-shows/music-bank/",
        "music-shows/m-countdown/",
        "music-shows/show-champion/",
        "music-shows/the-show/",
        "music-shows/inkigayo/",
        "music-shows/show-music-core/",
    ]

    shows = {
        0: "Music Bank",
        1: "M!Countdown",
        2: "Show Champion",
        3: "The Show",
        5: "Inkigayo",
        6: "Music Core",
    }

    result = [] # List of shows in order
    today = date.today() # - timedelta(days=1)
    for i, (k,v) in enumerate(shows.items()):
        diff = timedelta(days=k)
        show_date = intl_fmt(today-diff)
        tmp_show = Show(v, show_links[i], show_date)
        result.append(tmp_show)

    result.reverse() # Reverse returns none -_-
    return result

def intl_fmt(date):
    return date.strftime("%Y%m%d")

def show_table(reddit):
    shows = get_shows()

    for show in shows:
        try:
            wiki = reddit.subreddit('kpop').wiki[show.praw_url]
        except prawcore.exceptions.NotFound:
            show.no_broadcast = True
            continue
        try:
            markdown = wiki.content_md
        except:
            show.no_broadcast = True
            continue

    show_markdown = ""
    show_markdown += "Date | Performances | Discussion Thread | Winner\n"
    show_markdown += "--- | --- | --- | ---\n"
    for show in shows:
        if show.no_broadcast:
            show_markdown += "{} | {} | {} | {}\n".format(
                show.date,
                show.name,
                "No Broadcast.",
                "No Winner."
            )
        else:
            show_markdown += "{} | [{}]({}) | [Thread]({}) | [{}](/spoiler)\n" \
            .format(
                show.date,
                show.name,
                show.url,
                show.discussion_url,
                show.winner
            )
    return show_markdown

def main():
    r = praw.Reddit(client_id=config['Reddit']['ClientID'],
                    client_secret=config['Reddit']['ClientSecret'],
                    user_agent='TWIK Bot')

    print(show_table(r))

if __name__ == "__main__":
    main()
