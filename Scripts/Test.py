import time
import praw
import os
import atexit
from PostDatabase import PostDatabase
from PostTracker import PostTracker
import Defines
from Post import Post

#startup tracker
reddit = praw.Reddit(user_agent = 'thread_aggregator_for_statistics')

tracker = PostTracker(reddit)

print [str(x.trace) for x in tracker.database.posts]

steps = 0

while True:
	tracker.update()
	print 'finished step ' + str(steps)
	steps = steps + 1

print str(tracker.database)


