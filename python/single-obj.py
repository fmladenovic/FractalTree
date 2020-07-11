import math

PATH = '../pharo/objects1.txt'


class Node():
    def __init__(self, x, y, angle, connect_to, order_number = None, finished = False):
        self.x = x
        self.y = y
        self.angle = angle
        self.connect_to = connect_to
        self.order_number = order_number

        self.finished = finished

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.order_number) + ' ' + str(self.connect_to)

    def produce(self, base, angle):
        if self.finished:
            return None
        self.finished = True

        nodes = []

        angle1 =  self.angle + angle
        angle2 =  self.angle - angle

        x1 = self.x - base * math.sin(angle1)
        y1 = self.y - base * math.cos(angle1)

        x2 = self.x - base * math.sin(angle2)
        y2 = self.y - base * math.cos(angle2)

        nodes.append( Node( x1, y1, angle1, self.order_number ) )
        nodes.append( Node( x2, y2, angle2, self.order_number ) )

        return nodes

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
    nodes.append( Node( x, y, 0, 0, 1 ) ) # root
    nodes.append( Node( x, y - base, 0, 1, 2 ) ) # trunk
    while( base > end ):
        base = resize * base
        for i in range( len(nodes) - 1, 0, -1 ):
            new_nodes = nodes[i].produce( base, angle )
            if new_nodes != None:
                ind = len(nodes)
                new_nodes[0].order_number = ind + 1
                new_nodes[1].order_number = ind + 2
                nodes.extend(new_nodes) 
    
    write_list( nodes )

if __name__ == "__main__":
    base = 100
    resize = 2/3
    end = 20
    angle = 45
    x = 0
    y = 0

    tree(x, y, base, resize, end, angle)



