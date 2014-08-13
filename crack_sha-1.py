#coding:utf-8
import hashlib
import time
import os
filename = 'schedule.txt'
resultname = 'result.txt'
order = 0
cipher = 'd033e22ae348aeb5660fc2140aec35850c4da997'
ciphertest = '7110eda4d09e062aa5e4a390b0a572ac0d2c0220'
#dic = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
dic = ['0','1','2','3','4','5','6','7','8','9']

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
		run()
	except:
		pass
	finally:
		if os.path.isfile(filename):
			os.remove(filename)
		fp = open(filename,'w')
		fp.write(str(order-1))
		fp.close()

def run():
	global order
	found = False
	start = time.time()
	thistime = time.time()
	thisorder = order
	print 'start from %s' %order
	while found == False:
		text = str(order)
		order += 1
		if hashlib.sha1(text).hexdigest() == cipher:
			print text
			print "find!"
			if os.path.isfile(resultname):
				os.remove(resultname)
			fp = open(resultname,'w')
			fp.write(text)
			fp.close()
			found = True
		if order % 10000 == 0:
			if time.time() - thistime > 3:
				print '[%s items per second] current check text: %s ' % (((order - thisorder) // (time.time() - thistime)), text)
				thistime = time.time()
				thisorder = order


if __name__ == '__main__':
	main()