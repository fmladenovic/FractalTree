import math
import uuid
from multiprocessing import Process, Queue

PATH = '../pharo/py-multi.txt'
CONTINUE_WITH_CURRENT_PROCESS = -20


class Node():
    def __init__(self, x, y, parent_id):

        self.id = uuid.uuid1()
        self.parent_id = parent_id

        self.x = x
        self.y = y

        self.index = None
        self.ct_index = None

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.index) + ' ' + str(self.ct_index)


def tree(result_queue, spawn_controle, x, y, base, resize, end, angle, fork_angle, parent):
    result_queue.put(parent)
    if base > end:
        base = resize*base

        angle1 =  fork_angle - angle
        angle2 =  fork_angle + angle

        y1 = y + base * math.cos(angle1)
        x1 = x + (base* math.sin(angle1))
        node1 = Node(x1, y1, parent.id)

        y2 = y + base * math.cos(angle2)
        x2 = x + (base * math.sin(angle2))
        node2 = Node(x2, y2, parent.id)

        spawned = False
        if spawn_controle == 0:
            p1 = Process(target = tree, args = (result_queue, -1, x1, y1, base, resize, end, angle, angle1, node1) )
            p1.start()
            spawned = True
        elif spawn_controle == -1:
            p1 = Process(target = tree, args = (result_queue, -2, x1, y1, base, resize, end, angle, angle1, node1) )
            p1.start()
            spawned = True
        elif spawn_controle == 1:
            p1 = Process(target = tree, args = (result_queue, 2, x1, y1, base, resize, end, angle, angle1, node1) )
            p1.start()
            spawned = True
        else: 
            tree(result_queue, CONTINUE_WITH_CURRENT_PROCESS, x1, y1, base, resize, end, angle, angle1, node1)
        

        if spawn_controle == 0: tree(result_queue, 1, x2, y2, base, resize, end, angle, angle2, node2)
        else: tree(result_queue, CONTINUE_WITH_CURRENT_PROCESS, x2, y2, base, resize, end, angle, angle2, node2) 

        if spawned: p1.join()


def extract_nodes( queue ):
    nodes = []
    while queue.qsize() != 0:
        nodes.append(queue.get())
    return nodes

def flip( nodes ):
    for n in nodes:
        n.y = -n.y

def connect_nodes( nodes ):
    for i in range(len(nodes)):
        nodes[i].index = i + 1
    for i in range(1, len(nodes)):
        nodes[i].ct_index = index_of_id(nodes, nodes[i].parent_id) + 1
def index_of_id( nodes, id ):
    for i in range(len(nodes) ):
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

if __name__ == "__main__":
    x = 0
    y = 0
    base = 100
    resize = 2/3
    end = 20
    angle = 45

    result_queue = Queue()
    node = Node(x, y, 0)
    node.ct_index = 0
    result_queue.put(node)
    y = y + base
    node1 = Node(x, y, node.id)
    tree(result_queue, 0, x, y, base, resize, end, angle, 0, node1)

    nodes = extract_nodes(result_queue)
    connect_nodes(nodes)
    flip(nodes)
    write_list(nodes)
