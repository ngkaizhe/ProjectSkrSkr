from arrai import arrai

if __name__ == "__main__":
	a = arrai([1,2])
	b = arrai([[6], [5]])
	print("A: \n%s\n" % a)
	print("B: \n%s\n" % b)
	c = a.dot(b)
	print("A * B: \n%s\n" % c)
	print("A': \n%s\n" % a.transpose())
	d = a.dot(a.transpose())
	print("AA': \n%s\n" % d)
	#print(3*c)
