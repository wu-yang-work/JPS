from queue import PriorityQueue


class T():
    def __init(self):
        pass

    def t1(self, li):
        print('t1', li.queue)
        li.put(4)
        print('t1', li.queue)
        self.t2(li)
    def t2(self, li):
        print('t2 ', li.queue)
        li.put(5)
        print('t1', li.queue)
    def t(self, li):
        print('t ', li.queue)
        li.put(6)
        print('t', li.queue)
        self.t1(li)


if __name__ == '__main__':
    q = PriorityQueue()
    tt=T()
    tt.t(q)
    print(q.queue)


