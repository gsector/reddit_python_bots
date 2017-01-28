import praw
import re
import configparser


def main():
	config = configparser.RawConfigParser()
	config.read('aff_links_01.cfg')

	reddit_user = config.get('USER','reddit_user')
	reddit_password = config.get('USER','reddit_password')

	app_secret = config.get('APP','app_secret')
	app_name = config.get('APP','app_name')
	app_client_id = config.get('APP','app_client_id')

	reddit = praw.Reddit(client_id=app_client_id, client_secret=app_secret,
	                     password=reddit_password, user_agent=app_name,
	                     username=reddit_user)

	subr = config.get('SUBREDDIT','sub')

	link_re = re.compile('[htps:\/w.]*[\S]*amazon[\S]*[a-zA-Z0-9=]')
	tag_re = re.compile('\?[tT][aA]{0,1}[gG]{0,1}=[\S]*-[0-9][0-9]')

	# Process comments in a specific subreddit
	print('Running....')
	for comment in reddit.subreddit(subr).stream.comments():
		print(comment.body)
		for link in re.findall(link_re, comment.body):
			print(link)

if __name__ == '__main__':
	main()
	print('Done running')
