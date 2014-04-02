import re


def tweet_parser(tweet):
    """Takes in a unicode-formatted tweet and returns a dictionary of the
    game name, owner, opponent, move, and extra message.
    """
    tweet = tweet.encode()

    match = re.match(
        r'^@\w{11} (@(?P<opponent>[^\s]+) )?#(?P<game>\w+) (?P<move>[^\s]+) (?P<message>.*)$',
        tweet
    )

    if match:
        return match.groupdict()
    else:
        raise ValueError("Tweet not formatted correctly.")
