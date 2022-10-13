class fourcal:
    def __init__(self,first,second):
        self.setdata(first,second)

    def setdata(self,first,second):
        self.first=first
        self.second=second

    def sum(self):
        result=self.first+self.second
        return(result)
		
# a=fourcal()
# a.setdata(4,3)
a=fourcal(4,3)
print('first:',a.first)
print('second:',a.second)
print('sum: ',a.sum())

a.setdata(5,5)
print('first:',a.first)
print('second:',a.second)
print('sum: ',a.sum())
