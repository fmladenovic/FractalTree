import math
import uuid

PATH = '../pharo/py-single.txt'
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


def tree(nodes, x, y, base, resize, end, angle, fork_angle, parent ):
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

        nodes.append(node1)
        nodes.append(node2)

        tree( nodes, x1, y1, base, resize, end, angle, angle1, node1 )
        tree( nodes, x2, y2, base, resize, end, angle, angle2, node2 ) 



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

    nodes = []


    node = Node(x, y, 0)
    node.ct_index = 0

    y = y + base
    node1 = Node(x, y, node.id)

    nodes.append(node)
    nodes.append(node1)

    tree( nodes, x, y, base, resize, end, angle, 0, node1)

    connect_nodes(nodes)
    flip(nodes)
    write_list(nodes)
