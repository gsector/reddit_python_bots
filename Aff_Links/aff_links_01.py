import praw
import re
import configparser
from multiprocessing import Process


def process_comments():
	print('Processing Comments...')

	config = configparser.RawConfigParser()
	config.read('aff_links_01.cfg')

	reddit_user = config.get('USER', 'reddit_user')
	reddit_password = config.get('USER', 'reddit_password')

	app_secret = config.get('APP', 'app_secret')
	app_name = config.get('APP', 'app_name')
	app_client_id = config.get('APP', 'app_client_id')

	reddit = praw.Reddit(client_id=app_client_id, client_secret=app_secret,
						password=reddit_password, user_agent=app_name,
						username=reddit_user)

	subr = config.get('SUBREDDIT', 'sub')

	# Process comments in a specific subreddit
	for comment in reddit.subreddit(subr).stream.comments():
		amazon_links = find_amazon_links(comment.body)
		if amazon_links:
			print('Found Amazon link(s) in comment: ' + str(amazon_links))
			if find_affiliate_tags(amazon_links):
				print('** Affiliate link found! **')
				# comment.reply('Warning! An Affliate Link has been Detected in your post.')


def process_submissions():
	print('Processing Submissions...')

	config = configparser.RawConfigParser()
	config.read('aff_links_01.cfg')

	reddit_user = config.get('USER', 'reddit_user')
	reddit_password = config.get('USER', 'reddit_password')

	app_secret = config.get('APP', 'app_secret')
	app_name = config.get('APP', 'app_name')
	app_client_id = config.get('APP', 'app_client_id')

	reddit = praw.Reddit(client_id=app_client_id, client_secret=app_secret,
						password=reddit_password, user_agent=app_name,
						username=reddit_user)

	subr = config.get('SUBREDDIT', 'sub')

	# Process submissions in a specific subreddit
	for submission in reddit.subreddit(subr).stream.submissions():
		submission_text = submission.selftext + ' - ' + submission.url
		amazon_links = find_amazon_links(submission_text)
		if amazon_links:
			print('Found Amazon link(s) in submission: ' + str(amazon_links))
			if find_affiliate_tags(amazon_links):
				print('** Affiliate link found! **')
				# submission.reply('Warning! An Affliate Link has been Detected in your post.')



def find_affiliate_tags(link_list):
	'''
			(string) -> boolean

			Returns True when an affiliate link is found 
			within one of the links in the list of links.
			Else, returns False.
	'''

	tag_re = re.compile('\?[tT][aA]{0,1}[gG]{0,1}=[\S]*-[0-9][0-9]')

	for link in link_list:
		if re.findall(tag_re, link):
			return True
	return False


def find_amazon_links(blob):
	'''
			(string) -> List

			Returns a list of Amazon.com links within a string of text.
	'''

	link_re = re.compile('amazon\.[\S]*[a-zA-Z0-9=]')
	link_list = list()

	for link in re.findall(link_re, blob):
		link_list.append(link)

	return link_list


if __name__ == '__main__':
	Process(target=process_comments).start()
	Process(target=process_submissions).start()
