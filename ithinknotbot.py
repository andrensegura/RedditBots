import praw				#HEY, TRY USING get_comments(subreddit, gilded_only=False, *args, **kwargs) INSTEAD OF submission.comments
import time

LIMIT = 7

#connects to Reddit and identifies the script.
r = praw.Reddit(user_agent="Reddit API test bot 'ithinknotbot' by /u/bibbleskit")

#log in
r.login('ithinknotbot', '************')

#get the top 5 submissions for /r/all
allSubmissions = r.get_subreddit('askreddit').get_rising(limit=LIMIT)

a = 0;
while a < LIMIT:

	#get comments from a submission
	submission = next(allSubmissions)
	forest_comments = submission.comments #called it forest_comments because the comments are organized just like in a reddit submission
	flat_comments = praw.helpers.flatten_tree(forest_comments) #could have just combined the last two lines, but this is just for practice.
	#praw.helpers.flatten_tree flattens the forest so we can iterate through the comments easier.

	#find the string we are looking for
	opinion_strings = ["i think", "in my opinion"]
	already_done = []

	for comment in flat_comments:
		if not hasattr(comment, 'body'):
			continue
		if not isinstance(comment, praw.objects.Comment):
			continue
		comment_text = comment.body.lower()
		contains_opinion = any(string in comment_text for string in opinion_strings)
		if comment.id not in already_done and contains_opinion:
			comment.reply("You'd think that, but you'd be wrong.")
			already_done.append(comment.id)
			time.sleep(600)
	a = a + 1


#sleep so it doesnt run forever
time.sleep(1800)
