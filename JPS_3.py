from queue import PriorityQueue
import math


class Node(object):
    def __init__(self, x, y, parent=None, force_neighbours=None):
        parent = parent if parent else None
        force_neighbours = force_neighbours if force_neighbours else None
        self.x = x
        self.y = y
        self.parent = parent
        self.force_neighbours = force_neighbours


class JPS(object):
    def __init__(self, map_data, start, end, open=None):
        open = open if open else PriorityQueue()
        self.data = map_data
        self.start = Node(start[0], start[1])
        self.end = Node(end[0], end[1])
        self.open = open
        self.close = []
        self.path = []
        self.width = len(self.data)
        self.high = len(self.data[0])

    def is_walkable(self, x, y):
        # 1表示障碍物
        if 0 <= x < self.width and 0 <= y < self.high and self.data[x][y] == 0:
            return True
        return False

    def dir(self, v1, v2):
        v = v1 - v2
        if v > 0:
            return 1
        elif v == 0:
            return 0
        return -1

    def calc_euclidean(self, node1, node2):
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def calc_Manhattan(self, node1, node2):
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    def is_in_close(self, node):
        for temp in self.close:
            if node.x == temp.x and node.y == temp.y:
                return True
        return False

    def is_in_open(self, node):
        while not self.open.empty():
            temp = self.open.get()[1]
            if node.x == temp.x and node.y == temp.y:
                return True
        return False

    def search_hv(self, node, temp):
        if not self.is_walkable(temp.x, temp.y):
            return
        hori_dir = self.dir(temp.x, node.x)
        vert_dir = self.dir(temp.y, node.y)
        # 判断temp是否是跳点
        jump_node = self.is_jump_point(node, temp, hori_dir, vert_dir)
        if jump_node is not None:
            if not self.is_walkable(jump_node.x, jump_node.y):
                return
            f = self.calc_euclidean(jump_node, self.start) + self.calc_Manhattan(jump_node, self.end)
            jump_node.parent = node
            print('jump points:({0},{1})'.format(jump_node.x, jump_node.y))
            self.open.put((f, jump_node))
            print('open length:{0}'.format(self.open.qsize()))

        jump_node = self.jump_search_hv(temp, hori_dir, vert_dir)
        if jump_node is not None:
            if not self.is_walkable(jump_node.x, jump_node.y):
                return
            f = self.calc_euclidean(jump_node, self.start) + self.calc_Manhattan(jump_node, self.end)
            jump_node.parent = node
            print('find jump node:({0}, {1})'.format(jump_node.x, jump_node.y))
            print('jump points:({0},{1})'.format(jump_node.x, jump_node.y))
            self.open.put((f, jump_node))
            print('open length:{0}'.format(self.open.qsize()))

    def search_diag(self, node, temp):
        if temp is None or not self.is_walkable(temp.x, temp.y):
            return
        hori_dir = self.dir(temp.x, node.x)
        vert_dir = self.dir(temp.y, node.y)
        pre_node = node
        print('open length:{0}'.format(self.open.qsize()))
        print(self.open, id(self.open))
        print('    while     ')
        while True:
            if self.is_in_close(temp) or self.is_in_open(temp) or not self.is_walkable(temp.x, temp.y):
                break
            if self.is_jump_point(pre_node, temp, hori_dir, vert_dir):
                f = self.calc_euclidean(self.start, temp) + self.calc_Manhattan(self.end, temp)
                temp.parent = node
                print('open length:{0}'.format(self.open.qsize()))
                print(self.open, id(self.open))
                self.open.put((f, temp))
                print('jump points:({0},{1})'.format(temp.x, temp.y))
                print('open length:{0}'.format(self.open.qsize()))
                break
            pre_node = temp
            temp = Node(temp.x + hori_dir, temp.y + vert_dir)

    def check_node(self, node):
        print('check begin, open length:{0}'.format(self.open.qsize()))
        v_h = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        if node.parent is None:
            # 搜索上下左右四个方向
            print('parent is None, 开始水平、垂直搜索。。。')
            for dirct in v_h:
                temp = Node(node.x + dirct[0], node.y + dirct[1])
                self.search_hv(node, temp)
            print('parent is None, 水平、垂直搜索结束。。。')
        else:
            # 水平、垂直
            print('parent not None, 开始水平、垂直搜索。。。')
            hori_dir = self.dir(node.x, node.parent.x)
            vert_dir = self.dir(node.y, node.parent.y)
            if hori_dir != 0:
                print('沿X轴搜索。。。')
                temp = Node(node.x + hori_dir, node.y)
                self.search_hv(node, temp)
            if vert_dir != 0:
                print('沿Y轴搜索。。。')
                temp = Node(node.x, node.y + vert_dir)
                self.search_hv(node, temp)
            print('parent not None, 水平、垂直搜索结束。。。')

        print('?? open lenght:', self.open.qsize())

        if node.parent is None:
            # 搜索4个对角方向
            print('parent is None, 开始对角线搜索。。。')
            diag = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            for dirct in diag:
                temp = Node(node.x + dirct[0], node.y + dirct[1])
                self.search_diag(node, temp)
            print('parent is None, 对角线搜索结束。。。')
        else:
            print('parent not None, 开始对角线搜索。。。')
            hori_dir = self.dir(node.x, node.parent.x)
            vert_dir = self.dir(node.y, node.parent.y)
            if hori_dir != 0 and vert_dir != 0:
                temp = Node(node.x + hori_dir, node.y + vert_dir)
                self.search_diag(node, temp)
            print('parent not None, 对角线搜索结束。。。')

            print('?? open length:', self.open.qsize())
            # 遍历 node的 强迫邻居
            print('************ force neighbour **************')

            print('node:({0},{1})'.format(node.x, node.y))
            print('node force neighbours is None:', False if len(node.force_neighbours) > 0 else True)
            print('~~~~~~~ 开始朝force neighbour 搜索 ~~~~~~~~~~~')
            for force_neighbour in node.force_neighbours:
                print('node ({0},{1})'.format(node.x, node.y))
                print('node force neighbours ({0},{1})'.format(force_neighbour.x, force_neighbour.y))
                self.search_diag(node, force_neighbour)
            print('~~~~~~~ 朝force neighbour 搜索结束 ~~~~~~~~~~~')
        print('check after, open length:{0}'.format(self.open.qsize()))

    def search_path(self):
        if self.start.x == self.end.x and self.start.y == self.end.y:
            return
        # 计算开始节点的f值
        f = self.calc_euclidean(self.start, self.start) + self.calc_Manhattan(self.start, self.end)
        self.open.put((f, self.start))
        while not self.open.empty():
            # 取出当前F值最小的点
            cur_node = self.open.get()[1]
            self.close.append(cur_node)
            if cur_node.x == self.end.x and cur_node.y == self.end.y:
                return
            print('---------------begin------------------')
            print('search jump point:({0}, {1})'.format(cur_node.x, cur_node.y))
            if cur_node.parent:
                print('jump point parent:({0}, {1})'.format(cur_node.parent.x, cur_node.parent.y))
            else:
                print('jump point parent is None.')
            print('--------------------------------------')
            self.check_node(cur_node)

    def is_jump_point(self, node, temp, hori_dir, vert_dir):
        if not self.is_walkable(temp.x, temp.y) or temp is None:
            return
        # 一、起点和终点是跳点
        if (temp.x == self.start.x and temp.y == self.start.y) or (temp.x == self.end.x and temp.y == self.end.y):
            return temp
        # 二、如果temp有强迫邻居，则temp是跳点
        if self.has_force_neighbour(node, temp):
            return temp
        # 如果父节点在对角方向，节点node水平或垂直满足一、二
        if hori_dir != 0 and vert_dir != 0:
            return self.jump_search_hv(temp, hori_dir, vert_dir)
        return

    def jump_search_hv(self, node, hori_dir, vert_dir):
        i = node.x
        while hori_dir != 0:
            i += hori_dir
            temp = Node(i, node.y)
            if temp is None or not self.is_walkable(temp.x, temp.y):
                return
            if self.is_jump_point(node, temp, hori_dir, 0) is not None:
                return temp

        j = node.y
        while vert_dir != 0:
            j += vert_dir
            temp = Node(node.x, j)
            if temp is None or not self.is_walkable(temp.x, temp.y):
                return
            if self.is_jump_point(node, temp, 0, vert_dir) is not None:
                return temp
        return

    def has_force_neighbour(self, node, temp):
        if node is None or temp is None or not self.is_walkable(temp.x, temp.y):
            return False
        dirction = self.dir(temp.x, node.x), self.dir(temp.y, node.y)
        temp.force_neighbours = []
        # 水平、垂直
        if dirction[0] == 0 or dirction[1] == 0:
            result1 = self.check_hv_force_neighbour(temp, dirction, 1)
            result2 = self.check_hv_force_neighbour(temp, dirction, -1)
        else:
            result1 = self.check_diag_force_neighbour(temp, dirction, 1)
            result2 = self.check_diag_force_neighbour(temp, dirction, -1)
        return result2 or result1

    def check_hv_force_neighbour(self, node, dirction, sign):
        # 方向
        obstacle_dir = abs(dirction[1]) * sign, abs(dirction[0]) * sign
        obstacle = Node(node.x + obstacle_dir[0], node.y + obstacle_dir[1])
        neighbour = Node(obstacle.x + dirction[0], obstacle.y + dirction[1])

        if neighbour is None or not self.is_walkable(neighbour.x, neighbour.y):
            return False
        if obstacle is None or not self.is_walkable(obstacle.x, obstacle.y):
            neighbour.parent = node
            node.force_neighbours.append(neighbour)
            return True
        return False

    def check_diag_force_neighbour(self, node, dirction, sign):
        pre_node = Node(node.x - dirction[0], node.y - dirction[1])
        if sign == 1:
            obstacle_dir = dirction[0], 0
            neighbour_dir = dirction[0], 0
        else:
            obstacle_dir = 0, dirction[1]
            neighbour_dir = 0, dirction[1]
        obstacle = Node(pre_node.x + obstacle_dir[0], pre_node.y + obstacle_dir[1])
        neighbour = Node(obstacle.x + neighbour_dir[0], obstacle.y + neighbour_dir[1])
        if neighbour is None or not self.is_walkable(neighbour.x, neighbour.y):
            return False
        if obstacle is None or not self.is_walkable(obstacle.x, obstacle.y):
            neighbour.parent = node
            node.force_neighbours.append(neighbour)
            return True
        return False


if __name__ == '__main__':
    map_test = [[0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 0],
                ]
    start = (0, 0)
    end = (6, 6)
    jps = JPS(map_test, start, end)
    jps.search_path()
