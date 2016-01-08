#	CLASS THAT INTERACTS WITH REDDIT POST DATA
#
#
#	Posts store the following metadata about a post
#		-> id
#		-> time that tracking started
#		-> maximum score attained by the post
#		-> maximum number of comments attained by the post
#		-> post title
#		-> id of the user who posted
#		-> id of the subreddit the post was made in
#		-> link karma of the user who made the post
#		-> comment karma of the user who made the post
#		-> trace of score and number of comments over time
#
#	Posts are saved as a dictionary to a .mat file
#
#
#
#

import time
import praw
import scipy.io
import Defines

class Post:
	def __init__(self,post,variableNames=None):
		#if post is of type submission then we're creating a new post
		if isinstance(post,praw.objects.Submission):
			self.id = post.id
			self.time = time.time()
			self.maxScore = post.score
			self.maxComment = post.num_comments
			self.title = post.title
			self.subRedditID = post.subreddit_id
			self.userId = post.author.id
			self.linkKarma = post.author.link_karma
			self.commentKarma = post.author.comment_karma
			self.trace = [[self.time,post.score,post.num_comments]]

			#variables to determine when to stop tracking posts
			self.lastFluctuation = [self.time,post.score,post.num_comments]
			self.isAlive = True

		#if post is of type unicode then it's a filename and we should read from file
		elif isinstance(post,str) or isinstance(post,unicode):
			for key, value in scipy.io.loadmat(Defines.DataSourceDirectory + post,squeeze_me=True,variable_names=variableNames).items():
				#remove the header items
				if key.find('__') < 0:
					#convert traces into lists and preserve their dimension in the case that a trace only has one timestep in it
					#very specific... this should be made better
					if key.find('trace') >= 0 or key.find('lastFluctuation') >= 0:
						value = value.tolist()
						if key.find('trace') >= 0 and not isinstance(value[0],list):
							value = [value]

					setattr(self,key,value)

	#returns a string representation of the post
	def __str__(self):
		return '<' + self.id + ' : ' + self.title + ' : ' + str(self.maxScore) + '>'

	#updates the trace of post activity
	def update(self,post):
		#if the post is alive then update it
		if self.isAlive:
			up = [time.time(),post.score,post.num_comments]

			#if the update breaks any thread records, then record the new values
			if up[1] > self.maxScore:
				self.maxScore = up[1]

			if up[2] > self.maxComment:
				self.maxComment = up[2]

			if abs(up[1] - self.lastFluctuation[1]) > Defines.MinimumFluctuationForActivity:
				self.lastFluctuation = up

			#if the thread has been inactive for too long then kill it
			if time.time() - self.lastFluctuation[0] > Defines.MaximumInactivityTime:
				self.isAlive = False

			#record the update
			self.trace.append(up)

	#write the post to a file whose name is given by the post id
	def write(self):
		scipy.io.savemat(Defines.DataSourceDirectory + self.id, vars(self))


