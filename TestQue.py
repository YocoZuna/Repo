import multiprocessing
import time

class Elo(multiprocessing.Process):
    def __init__(self,que):
        self.queue = que
        multiprocessing.Process.__init__(self)
    def square_list(self,):
        """
        function to square a given list
        """
        # append squares of mylist to queue
        while 1:
            self.queue.put(2*2)
  
def print_queue(x):
    """
    function to print queue elements
    """

    while 1:
        while not x.empty():
            print(x.get())

  
if __name__ == "__main__":
    # input list
    mylist = [1,2,3,4]
    q  =  multiprocessing.Queue()
    # creating multiprocessing Queue
    q = multiprocessing.Queue()
    siema = Elo(q)
    kutank = []
    # creating new processes
    #p1 = multiprocessing.Process(target=siema.square_list)
    #p2 = multiprocessing.Process(target=print_queue,args=(q,))
    ResultArray = [[1,111,2],[3,222,4],[5,333,6],[7,444,8],[9,555,10],[11,666,12]]
    for i in ResultArray:
        for y in i:
            kutank.append(y)
    PrevValues = [[],[],[],[],[],[]]

    for i in range(0,len(PrevValues)):
        PrevValues[i].append(ResultArray[i][0:2])
    ResultArray = [[11,22],[33,44],[55,66],[77,88],[99,100],[110,120]]
    print(f"***Orginal Result Arra*****{ResultArray}")
    print(f"***Orginal Prev Arra*****{PrevValues}")
    """    for i in range(0,len(PrevValues)):
            tempIter = 0
            for y in PrevValues:
                for z in range(0,len(y)):
                    ResultArray[i].insert(tempIter,PrevValues[y][z])
                    tempIter +=1
                    print(f"MOdif result array *****{ResultArray}")"""
    for z in range(0,len(ResultArray)):
        tempIter = 0
        for y in range(0,2):
            ResultArray[z].insert(tempIter,PrevValues[z][0][y])
            print(ResultArray)
            tempIter+=1
    print(f"MOdif result array *****{ResultArray}")
    # running process p1 to square list
    #p1.start()
    # running process p2 to get queue elements
kutas = []
for i in range(0,32):
    kutas.append(i)
print(kutas)

