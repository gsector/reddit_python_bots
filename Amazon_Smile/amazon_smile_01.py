import praw
import re
import configparser


config = configparser.RawConfigParser()
config.read('amazon_smile_01.cfg')

reddit_user = config.get('USER', 'reddit_user')
reddit_password = config.get('USER', 'reddit_password')

app_secret = config.get('APP', 'app_secret')
app_name = config.get('APP', 'app_name')
app_client_id = config.get('APP', 'app_client_id')

reddit = praw.Reddit(client_id=app_client_id, client_secret=app_secret,
                     password=reddit_password, user_agent=app_name,
                     username=reddit_user)

p = re.compile('([htps:\/w.]+amazon.com\/.*)')


def last_char_test(c):
    '''
            char -> boolean

            Returns true when the last character in a string
            is valid for a url last character
    '''
    return c.isalpha() or c.isdigit() or c in '?='


def extract_url(raw_url):
    '''
            string -> string

            Takes a string, extracts the first part before a space if there is one,
            and then removes last characters until it hits a valid url character.
    '''

    try:
        all_pieces = raw_url.split(' ')
        only_url = all_pieces[0]
    except:
        only_url = raw_url

    while last_char_test(only_url[-1]) is False:
        try:
            only_url = only_url[:-1]
        except:
            return None

    return only_url


def create_reply(url):
    text = 'AmazonSmile Link'
    reftag = '/?tag=smile.reddit-20'
    tagline = '\n\nUse this AmazonSmile link to donate a part of your purchase to charity.'

    # reply_text = '[AmazonSmile Link]({}{})^^[no-ref]({})'.format(url,reftag,url)
    # reply_text = '[AmazonSmile Link]({}{})'.format(url,reftag)
    reply_text = '[AmazonSmile Link]({})'.format(url)
    reply_text = reply_text + tagline

    return reply_text


def process_comment(comment):
    amazon_matches = p.findall(comment)

    # If 1 amazon link is found...
    if len(amazon_matches) == 1:
        # Clean up the url....
        raw_url = amazon_matches[0]
        url = extract_url(raw_url)
        if 'smile.amazon' in url:
            return None
        # Add smile link stuff
        url = url.replace('amazon.', 'smile.amazon.')
        if 'www.smile' in url:
            url = url.replace('www.smile.', 'smile.')

        return create_reply(url)
    else:
        return None


def post_comment(comment, reply_text):
    try:
        comment.reply(reply_text)
        print('Comment Posted')
    except:
        print('Error posting')


for comment in reddit.subreddit('all').stream.comments():
    reply_text = process_comment(comment.body)
    if reply_text is not None:
        post_comment(comment, reply_text)
