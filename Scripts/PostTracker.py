#	CLASS THAT

import time
from Post import Post
from PostDatabase import PostDatabase
import Defines
import os.path


class PostTracker:

	def __init__(self,reddit,subreddits=['worldnews','pics','funny','aww','todayilearned']):
		self.reddit = reddit
		self.database = PostDatabase(mode='w')
		self.subreddits = subreddits

		#post that we are will update on the next call to update()
		self.currentPost = 0
		self.lastWrite = 0
		self.lastUpdate = time.time()

		#check to see whether a backup file exists
		if os.path.isfile(Defines.BackupFile):
			print 'backup exists... reading backup.'
			self.database.readBackup()
		else:
			print 'no backup... initializing'
			#load the raw post data from the subreddits
			posts = [[y for y in reddit.get_subreddit(x).get_new(limit=Defines.MaximumSubredditDepth)] for x in subreddits]

			#go through each post, add the author information and then add it to the database
			for x in posts:
				for y in x:
					y.author = reddit.get_redditor(y.author.name)
					self.database.addPost(Post(y))


	def update(self):
		#if there aren't 100 posts left to update then only update up to the end of the list
		#and see if we need to add anymore posts to track
		querySize = min(Defines.MaximumQuerySize,len(self.database.posts) - self.currentPost)

		#go through and update the posts
		updatedPosts = [y for y in self.reddit.get_submissions(['t3_'+str(x.id) for x in self.database.posts[self.currentPost:self.currentPost+querySize]])]

		for x in range(self.currentPost,self.currentPost+querySize):
			self.database.posts[x].update(updatedPosts[x-self.currentPost])

		self.currentPost += querySize

		#if we reached the end of the set of posts, restart and see if we need to scan for more, new posts
		#then if we have waited more than the minimum time between writes, write the data.
		if self.currentPost >= len(self.database.posts):
			print 'updated all posts.'
			self.currentPost = 0

			#if we need to load more posts then load them
			if len(self.database.posts) < Defines.MaximumConcurrentPosts:
				#load the raw post data from the subreddits
				posts = [[y for y in self.reddit.get_subreddit(x).get_new(limit=Defines.MaximumSubredditDepth)] for x in self.subreddits]

				#go through the posts and add any that aren't currently in our list
				for x in posts:
					for y in x:
						#stop if we have filled up the set of posts to track
						if len(self.database.posts) >= Defines.MaximumConcurrentPosts:
							break

						#check whether the current post is redundent
						doubled = False

						for z in self.database.posts:
							if z.id == y.id:
								doubled = True

						#if it is not, then add it to the set of posts
						if not doubled:
							y.author = self.reddit.get_redditor(y.author.name)
							self.database.addPost(Post(y))
							print 'adding post to trace.'

			#if too much time has ellapsed then write the current state of all of the posts
			if time.time() - self.lastWrite > Defines.SaveRate:
				self.database.writePosts()
				self.lastWrite = time.time()
				print 'posts written'

			#if any posts have expired then remove them
			self.database.posts[:] = [x for x in self.database.posts if x.isAlive]

			#if we need to then write the backup file
			if time.time() - self.lastUpdate > Defines.BackupFrequency:
				self.database.writeBackup()

			if time.time() - self.lastUpdate < Defines.CollectionRate:
				print 'pausing to update for ' + str(Defines.CollectionRate - (time.time() - self.lastUpdate))
				time.sleep(Defines.CollectionRate - time.time() + self.lastUpdate)

			self.lastUpdate = time.time()









