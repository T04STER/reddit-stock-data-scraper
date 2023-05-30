import logging
import re
from collections import Counter
from typing import List, Pattern
from praw import Reddit
from praw.models import ListingGenerator, Submission
from praw.models.comment_forest import CommentForest


class RedditScraper:
    __ticker_symbol_pattern = r' ([A-Z]{3,7}) '

    def __init__(self, reddit_client: Reddit, subreddits: List[str], posts_per_request: int = 100):
        self.reddit_client: Reddit = reddit_client
        self.subreddits: List[str] = subreddits
        self.posts_per_request: int = posts_per_request
        self.complied_regex: Pattern[str] = re.compile(self.__ticker_symbol_pattern)

    def scrap(self) -> List:
        logging.info('Scrapping reddit started')
        ticker_count_dicts = [self.__scrap_subreddit(subreddit) for subreddit in self.subreddits]
        merged_counter = Counter()
        for counter in ticker_count_dicts:
            merged_counter.update(counter)
        return merged_counter.most_common()

    def __scrap_subreddit(self, subreddit_name) -> Counter:
        submissions: ListingGenerator = self.reddit_client.subreddit(subreddit_name).top(limit=self.posts_per_request)

        ticker_symbol_counter = Counter()

        submission: Submission
        for submission in submissions:
            ticker_symbol_counter.update(self.__get_tickers_from_text(submission.title))
            ticker_symbol_counter += (self.__get_tickers_from_text(submission.selftext))
            ticker_symbol_counter += (self.__get_tickers_from_comments(submission.comments))

        return ticker_symbol_counter

    def __get_tickers_from_text(self, text: str) -> Counter:
        matches = self.complied_regex.findall(text)
        ticker_counter = Counter()
        for ticker in matches:
            ticker_counter[ticker] += 1
        return ticker_counter

    def __get_tickers_from_comments(self, comments: CommentForest):
        ticker_counter = Counter()
        for comment in comments.list():
            comment_submission = comment.submission
            comment_text = comment_submission.selftext
            ticker_counter += self.__get_tickers_from_text(comment_text)
            replies = comment_submission.comments
            for reply in replies:
                reply_text = reply.submission.selftext
                ticker_counter += self.__get_tickers_from_text(reply_text)

        return ticker_counter

