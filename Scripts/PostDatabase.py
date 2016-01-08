#	CLASS THAT MANAGES POST DATA COLLECTED FROM REDDIT
#
#	Files will be titled with their post id.
#
#	Functions:
#
#		openPosts(self,posts):
#			Function loads posts based on a list of post ids.
#
#		clearPosts(self):
#			Function clears the current dictionary of posts
#
#		readPosts(self,variableNames):
#			Reads in requested variables from all posts (based on variableNames)
#			so that critera may be easily filtered for
#
#		addPost(self,post):
#			Adds a new post to the dictionary. Only
#
#		writePosts(self):
#			Writes all posts to files
#

import Defines
import os
from Post import Post

class PostDatabase:
	def __init__(self,mode='r'):
		self.mode = mode
		self.posts = list()

	def openPosts(self,posts):
		self.posts.extend([Post(x) for x in posts])


	def clearPosts(self):
		if self.mode=='r':
			del self.posts[:]

	def readPosts(self,variableNames=None):
		filenames = os.listdir(Defines.DataSourceDirectory)
		for x in filenames:
				if x.endswith('.mat'):
					yield Post(x[:len(x)-4],variableNames)

	def __str__(self):
		return str([str(x) for x in self.posts])

	def addPost(self,post):
		if self.mode=='w':
			self.posts.append(post)

	def writePosts(self):
		if self.mode=='w':
			for x in self.posts:
				x.write()

	def writeBackup(self):
		if self.mode=='w':
			self.writePosts()
			outputFile = open(Defines.BackupFile,'w')

			for x in self.posts:
				outputFile.write(str(x.id) + '\n')

			outputFile.close()

	def readBackup(self):
		outputFile = open(Defines.BackupFile,'r')

		self.clearPosts()

		self.openPosts([line[:len(line)-1] for line in outputFile])
		outputFile.close()






