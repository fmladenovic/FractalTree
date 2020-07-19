import math
import time
import uuid
from multiprocessing import Process, Queue



PATH = '../pharo/test.txt'


class Node():
    def __init__(self, x, y, angle, parent_id, index = None, ct_index = None):

        self.id = uuid.uuid1()
        self.paren_id = parent_id 

        self.x = x
        self.y = y
        self.angle = angle

        self.index = index
        self.ct_index = ct_index

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.index) + ' ' + str(self.ct_index)

    def produce(self, nodes, base, resize, end, angle):
        if base > end:
            base = base * resize
            angle1 =  self.angle + angle
            angle2 =  self.angle - angle

            x1 = self.x - base * math.sin(angle1)
            y1 = self.y - base * math.cos(angle1)

            x2 = self.x - base * math.sin(angle2)
            y2 = self.y - base * math.cos(angle2)

            node1 = Node( x1, y1, angle1, self.id )
            nodes.put( node1 )
            node1.produce( nodes, base, resize, end, angle )

            node2 = Node( x2, y2, angle2, self.id )
            nodes.put( node2 )
            if nodes.qsize() == 1:
                p = Process( target = node2.produce, args = (nodes, base, resize, end, angle) )
                p.start()
                p.join()
            else: 
                node2.produce( nodes, base, resize, end, angle )


def connect_nodes( nodes ):
    for i in range(2, len(nodes)):
        nodes[i].index = i + 1
    for i in range(2, len(nodes)):
        nodes[i].ct_index = index_of_id(nodes, nodes[i].paren_id) + 1

def index_of_id( nodes, id ):
    for i in range( len(nodes) ):
        if nodes[i].id == id:
            return i
    return None


def write_list( nodes ):
    f = open(PATH, "a")
    f.truncate(0)
    file_content = ''
    for i in range( len(nodes) ):
        if i == 0 :
            file_content += str(nodes[i])
        else:
            file_content += '|' + str(nodes[i])
    f.write(file_content)
    f.close()


def tree(x, y, base = 100, resize = 1/2, end = 10, angle = 45): 
    nodes = []
    nodes.append( Node( x, y, 0, None, 1, ct_index=0 ) )
    nodes.append( Node( x, y - base, 0, nodes[0].id, 2, ct_index = 1) )

    nodes_q = Queue()
    nodes[len(nodes) - 1].produce(nodes_q, base, resize, end, angle)

    while nodes_q.qsize() != 0:
        nodes.append(nodes_q.get())
    
    return nodes

def run():
    base = 100
    resize = 2/3
    end = 10
    angle = 45
    x = 0
    y = 0

    start = time.perf_counter()

    nodes = tree(x, y, base, resize, end, angle)
    
    end = time.perf_counter()
    print(f'Finish in {round(end-start, 5)} secounds(s)')


    print(f'Preparing for pharo...')
    connect_nodes(nodes)
    write_list( nodes )


if __name__ == "__main__":
    run()


