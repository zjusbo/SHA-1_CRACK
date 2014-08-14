#coding:utf-8
import hashlib
import time
import os
import threading
filename = 'schedule.txt'
resultname = 'result.txt'
order = 0
found = False
threadNumber = 10
lock  = threading.Lock()
text = ""
roundNumber = 0
roundNumberLock = threading.Lock()
cipher = '4823bf9770f7d55fe63839e8ee4a8331c5bfb901'
ciphertest = '7110eda4d09e062aa5e4a390b0a572ac0d2c0220'
#dic = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#dic = ['0','1','2','3','4','5','6','7','8','9']
dic = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

class Cracker(threading.Thread):
	def __init__(self, event, roundRange):
		threading.Thread.__init__(self)
		self.roundRange = roundRange
		self.start = order
		self.threadEvent = event
		
	def run(self):
		print 'hi'
		global found, order, lock, text, cipher
		self.roundStart = order
		print 'hi'
		while found == False:
			lock.acquire()
			self.start = order
			order += self.roundRange
			lock.release()
			self.order = self.start
			while self.order <= self.start - self.roundRange and found == False:
				self.text= generateText(order)
				if self.threadEvent.isSet():
					roundNumberLock.acquire()
					roundNumber +=  self.order - self.roundStart
					roundNumberLock.release()
					self.roundStart = self.order
					text = self.text
					self.threadEvent.clear()
				if hashlib.sha1(self.text).hexdigest() == cipher:
					print self.text
					print "find!"
					if os.path.isfile(resultname):
						os.remove(resultname)
						fp = open(resultname,'w')
						fp.write(self.text)
						fp.close()
					found = True
				order += 1

def generateText(order):
	text = ''
	if order == 0:
		return '0'
	while order != 0:
		text = dic[order % len(dic)] + text
		order /= len(dic)
	return text
def main():
	global order
	if os.path.isfile(filename):
		fp = open(filename,'r+')
		order = fp.readline()
		order = int(order)
		fp.close()
	try:
		myRun(cipher)
	except:
		import traceback
		print "Generic exception: " + traceback.format_exc()
	finally:
		if os.path.isfile(filename):
			os.remove(filename)
		fp = open(filename,'w')
		fp.write(str(order-1))
		fp.close()

def myRun(cipher):
	global roundNumber, threadNumber, text, found
	print 'start from %s' % order
	threadEvents = []
	for x in xrange(1,threadNumber):
		threadEvents.append(threading.Event())
		a = Cracker(threadEvents[-1],10000)
		a.start()
		print x
	startTime = time.time()
	while found == False:
		if time.time() - startTime > 2:
			roundNumberLock.acquire()
			roundNumber = 0
			roundNumberLock.release()
			for event in threadEvents:
				event.set()
			for event in threadEvents:
				event.wait()
			thisTime = time.time()
			print '[%s threads] [%s items per second] current check text: %s ' % (threadNumber, roundNumber // (thisTime - startTime), text)
			startTime = thisTime
if __name__ == '__main__':
	main()