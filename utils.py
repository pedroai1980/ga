import numpy as np 

def allow(x, k):
	return True 

def lesser(x, k):
	return True if x<k else False

def lesser_equal(x, k):
	return True if x<=k else False

def greater(x, k):
	return True if x>k else False

def greater_equal(x, k):
	return True if x>=k else False

def equal(x, k):
	return True if x==k else False

def range_include(x, k):
	k1, k2 = k
	return True if (x>=k1 and x<=k2) else False

def range_exclude(x, k):
	k1, k2 = k
	return True if (x>=k1 and x<=k2) else False