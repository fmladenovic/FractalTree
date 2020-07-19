import math
import time
import uuid
import concurrent.futures

PATH = '../pharo/test.txt'
PROCCESSES_COUNT = 7


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

    def produce(self, base, angle):
        nodes = []

        angle1 =  self.angle + angle
        angle2 =  self.angle - angle

        x1 = self.x - base * math.sin(angle1)
        y1 = self.y - base * math.cos(angle1)

        x2 = self.x - base * math.sin(angle2)
        y2 = self.y - base * math.cos(angle2)

        nodes.append( Node( x1, y1, angle1, self.id ) )
        nodes.append( Node( x2, y2, angle2, self.id ) )

        return nodes

def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))

def extract_nodes( generations ):
    nodes = []
    for generation in generations:
        for node in generation:
            nodes.append(node)
    return nodes

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


def process_job(nodes, base, angle ):
    new_nodes = []
    for i in range( len(nodes) ):
        new_nodes.extend(nodes[i].produce( base, angle ))
    return new_nodes

def tree(x, y, base = 100, resize = 1/2, end = 10, angle = 45): 
    generations = []
    generations.append( [Node( x, y, 0, None, 1, ct_index=0 )] )
    generations.append( [Node( x, y - base, 0, generations[0][0].id, 2, ct_index = 1)] )

    while( base > end ):
        base = resize * base

        processes_lists = list(chunker_list(generations[len(generations) - 1], PROCCESSES_COUNT))

        nodes = []
        with concurrent.futures.ProcessPoolExecutor(7) as executor:
            results = [executor.submit(process_job,  nodes_for_method, base, angle ) for nodes_for_method in processes_lists ]
            for f in concurrent.futures.as_completed(results):
                nodes.extend(f.result())

        generations.append(nodes)

    return generations

def run():
    base = 100
    resize = 2/3
    end = 10
    angle = 45
    x = 0
    y = 0

    start = time.perf_counter()

    generations = tree(x, y, base, resize, end, angle)
    
    end = time.perf_counter()
    print(f'Finish in {round(end-start, 5)} secounds(s)')


    print(f'Preparing for pharo...')
    nodes = extract_nodes( generations )
    connect_nodes(nodes)
    write_list( nodes )


if __name__ == "__main__":
    run()


