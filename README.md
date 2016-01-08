# Reddit Research Bot

Reddit is a great website both as a distraction and as a large dataset. I wanted to see if I could predict which posts would accrue a large number of upvotes by analyzing words in the title and comments as well as the initial rate of upvotes. To start studying this question I wrote some scripts in python to scan certain subreddits and construct a database of post upvotes vs time. I left the code running on an amazon EC2 instance for some time and ended up tracing over 7000 posts from their creation until they stopped getting upvotes. You can see these traces in the Plots directory.

The bulk of the code involves a Post class which stores posts, a PostDatabase class which writes posts as matlab data files and gracefully handles reading/writing a backup file in the event of a crash, a PostTracker class which interfaces with the PRAW library to keep information about post upvotes vs time. It would be interesting to try to correlate post titles with overall score using NLP methods.

Using the library is fairly easy. Here is an example.
```
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
```
