import configparser
import praw
import re

config = configparser.ConfigParser()
config.read('config.ini')

QUERIES = [
    'flair:"Discussion"',
    'flair:"news" OR flair:"rumor"',
    'flair:"song cover" OR flair:"dance cover" OR flair:"live" OR flair:"dance practice"',
]

class Link():
    def __init__(self, title, link, votes, num_comments):
        self.title = title
        self.link = link
        self.votes = votes
        self.num_comments = num_comments
        self.flair = ""

def get_discussions(reddit):
    discussions = []
    for submission in reddit.subreddit('kpop').search(
            query=QUERIES[0],
            sort="top",
            time_filter="week",
            limit=10):
        submission.comments.replace_more(limit=None, threshold=0)
        link = Link(
            submission.title,
            submission.permalink,
            submission.score,
            len(submission.comments.list())
        )
        discussions.append(link)
    return discussions[:10]

def get_news(reddit):
    stories = []
    for submission in reddit.subreddit('kpop').search(
            query=QUERIES[1],
            sort="top",
            time_filter="week",
            limit=10):
        submission.comments.replace_more(limit=None, threshold=0)
        link = Link(
            submission.title,
            submission.permalink,
            submission.score,
            len(submission.comments.list())
        )
        stories.append(link)
    return stories[:10]

def get_performances(reddit):
    performances = []
    for submission in reddit.subreddit('kpop').search(
            query=QUERIES[2],
            sort="top",
            time_filter="week",
            limit=10):
        submission.comments.replace_more(limit=None, threshold=0)
        link = Link(
            submission.title,
            submission.permalink,
            submission.score,
            len(submission.comments.list())
        )
        link.flair = submission.link_flair_text
        performances.append(link)
    return performances[:10]

def main():
    r = praw.Reddit(client_id=config['Reddit']['ClientID'],
                    client_secret=config['Reddit']['ClientSecret'],
                    user_agent='TWIK Bot')

    print("#### TOP 5 STORIES")
    print("| # | Votes | Thread | Comments |")
    print(":--|:--|:--|:--")
    for index, story in enumerate(get_news(r)):
        print("| {} | (+{}) | [{}]({}) | {} comments".format(
            index+1,
            story.votes,
            story.title,
            story.link,
            story.num_comments
        ))


    print("\n#### TOP 5 PERFORMANCES")
    print("| # | Votes | Thread | Comments |")
    print(":--|:--|:--|:--")
    for index, performance in enumerate(get_performances(r)):
        print("| {} | (+{}) | [{} {}]({}) | {} comments".format(
            index+1,
            performance.votes,
            performance.flair,
            performance.title,
            performance.link,
            performance.num_comments
        ))

    print("\n#### TOP 5 DISCUSSIONS")
    print("| # | Votes | Thread | Comments |")
    print(":--|:--|:--|:--")
    for index, discussion in enumerate(get_discussions(r)):
        print("| {} | (+{}) | [{}]({}) | {} comments".format(
            index+1,
            discussion.votes,
            discussion.title,
            discussion.link,
            discussion.num_comments
        ))

if __name__ == "__main__":
    main()
