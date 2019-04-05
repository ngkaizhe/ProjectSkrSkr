from arrai import Arrai
import arrai as ar
if __name__ == "__main__":
	a = Arrai([1,2])
	b = Arrai([[6], [5]])
	print("A: \n%s\n" % a)
	print("B: \n%s\n" % b)
	c = a.mul(b)
	print("A * B: \n%s\n" % c)
	print("A': \n%s\n" % a.transpose())
	d = a.mul(a.transpose())
	print("AA': \n%s\n" % d)

	e = Arrai(3)
	print(10+a)
	print(a)
	print(a  * e)
	print(e * a)
	print(a)
	print(a-5)
	print(a*3)
	print(a*3^33)
