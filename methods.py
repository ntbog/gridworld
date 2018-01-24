from __future__ import print_function
#Use priority queues from Python libraries, don't waste time implementing your own
#Check https://docs.python.org/2/library/heapq.html
from heapq import *

class Agent:
    def __init__(self, grid, start, goal, type):
        self.actions = [(0,-1),(-1,0),(0,1),(1,0)]
        self.grid = grid
        self.came_from = {}
        self.checked = []
        self.start = start
        self.grid.nodes[start[0]][start[0]].start = True
        self.goal = goal
        self.grid.nodes[goal[0]][goal[1]].goal = True
        self.new_plan(type)
    def new_plan(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        if self.type == "dfs" :
            self.frontier = [self.start]
            self.checked = []
        elif self.type == "bfs":
            self.frontier = [self.start]
            self.checked = []
        elif self.type == "ucs":
            self.frontier = []
            self.checked = []
            self.gdict = {self.start: 0}
            heappush(self.frontier, (0, self.start))
            #[Hint] you need a dictionary that keeps track of cost
            #[Hint] you probably also need something like this: heappush(self.frontier, (0, self.start))
        elif self.type == "astar":
            self.frontier = []
            self.checked = []
            self.gdict = {self.start: 0}
            heappush(self.frontier, (0, self.start))
    def show_result(self):
        current = self.goal
        while not current == self.start:
            current = self.came_from[current]
            self.grid.nodes[current[0]][current[1]].in_path = True
    def make_step(self):
        #[Hint] dfs and bfs should look very similar
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        #[Hint] ucs and astar should look very similar
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()
    def dfs_step(self):
        #... see if it ran out of options
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop()
        print("popped: ", current)
        #... keep track
        self.grid.nodes[current[0]][current[1]].checked = True
        self.grid.nodes[current[0]][current[1]].frontier = False
        self.checked.append(current)
        #... loop through possible next step
        for i, j in self.actions:
            #... tests the 4 action relative to current
            nextstep = (current[0]+i, current[1]+j)
            #... prevent revisiting
            #See what happens if you disable this check here
            if nextstep in self.checked or nextstep in self.frontier:
                print("expanded before: ", nextstep)
                continue
            #... check if it's in boundaries of the grid
            if 0 <= nextstep[0] < self.grid.row_range:
                if 0 <= nextstep[1] < self.grid.col_range:
                    #... check if puddle
                    if not self.grid.nodes[nextstep[0]][nextstep[1]].puddle:
                        if nextstep == self.goal:
                            self.finished = True
                        #... add to the frontier which will be traversed to eventually
                        self.frontier.append(nextstep)
                        #... book keeping
                        self.grid.nodes[nextstep[0]][nextstep[1]].frontier = True
                        #... book keeping
                        self.came_from[nextstep] = current
                        print("pushed: ", nextstep)
                    else:
                        print("puddle at: ", nextstep)
                else:
                    print("out of column range: ", nextstep)
            else:
                print("out of row range: ", nextstep)
    def bfs_step(self):
        #... finished instead of failed
        if not self.frontier:
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()
        print("popped: ", current)
        #... keep track
        self.grid.nodes[current[0]][current[1]].checked = True
        self.grid.nodes[current[0]][current[1]].frontier = False
        self.checked.append(current)
        #... loop through possible next step
        for i, j in self.actions:
            #... tests the 4 action relative to current
            nextstep = (current[0]+i, current[1]+j)
            #... prevent from visiting again
            #See what happens if you disable this check here
            if nextstep in self.checked or nextstep in self.frontier:
                print("expanded before: ", nextstep)
                continue
            #... check if it's in boundaries of the grid
            if 0 <= nextstep[0] < self.grid.row_range:
                if 0 <= nextstep[1] < self.grid.col_range:
                    #... check if puddle
                    if not self.grid.nodes[nextstep[0]][nextstep[1]].puddle:
                        if nextstep == self.goal:
                            self.finished = True
                        #... insert a pair this time
                        self.frontier.insert(0, nextstep)
                        self.grid.nodes[nextstep[0]][nextstep[1]].frontier = True
                        self.came_from[nextstep] = current
                        print("pushed: ", nextstep)
                    else:
                        print("puddle at: ", nextstep)
                else:
                    print("out of column range: ", nextstep)
            else:
                print("out of row range: ", nextstep)
    def ucs_step(self):
        #[Hint] you can get the cost of a node by node.cost()
        #... see if it ran out of options
        if not self.frontier:
            self.finished = True
            print("no path")
            return
        current = heappop(self.frontier)[1]
        current_cost = self.gdict[current]
        print("popped: ", current, " cost: ", current_cost)
        #... keep track
        self.grid.nodes[current[0]][current[1]].checked = True
        self.grid.nodes[current[0]][current[1]].frontier = False
        self.checked.append(current)
        #... loop through possible next step
        for i, j in self.actions:
            #... tests the 4 action relative to current
            nextstep = (current[0]+i, current[1]+j)
            #... prevent from visiting again
            #See what happens if you disable this check here
            #if nextstep in self.checked or nextstep in self.frontier:
            #    print("expanded before: ", nextstep)
            #    continue
            #... check if it's in boundaries of the grid
            if 0 <= nextstep[0] < self.grid.row_range:
                if 0 <= nextstep[1] < self.grid.col_range:
                    #... check if puddle
                    if not self.grid.nodes[nextstep[0]][nextstep[1]].puddle:
                        if not nextstep in self.checked:
                            if nextstep == self.goal:
                                self.finished = True
                            #   keeping track of cost
                            #   typical UCS expands on the lowest cost
                            next_cost = current_cost + self.grid.nodes[nextstep[0]][nextstep[1]].cost()
                            self.gdict[nextstep] = next_cost
                            if not (next_cost, nextstep) in self.frontier:
                                heappush(self.frontier, (self.gdict[nextstep],nextstep))
                                self.grid.nodes[nextstep[0]][nextstep[1]].frontier = True
                                self.came_from[nextstep] = current
                                print("pushed: ", nextstep)
                            else:
                                print("expanded before: ", nextstep)
                        else:
                            print("checked before: ", nextstep)
                    else:
                        print("puddle at: ", nextstep)
                else:
                    print("out of column range: ", nextstep)
            else:
                print("out of row range: ", nextstep)
    #[Hint] you need to declare a heuristic function for Astar
    def h_val(self, a, b):
        c = abs(a[0] - b[0])
        d = abs(a[1] - b[1])
        # return can be multiplied for faster but less exhaustive search
        return (c + d)
    def astar_step(self):
        #[Hint] you can get the cost of a node by node.cost()
        #... see if it ran out of options
        if not self.frontier:
            self.finished = True
            print("no path")
            return
        current = heappop(self.frontier)[1]
        current_cost = self.gdict[current]
        print("popped: ", current, " cost: ", current_cost)
        #... keep track
        self.grid.nodes[current[0]][current[1]].checked = True
        self.grid.nodes[current[0]][current[1]].frontier = False
        self.checked.append(current)
        #... loop through possible next step
        for i, j in self.actions:
            #... tests the 4 action relative to current
            nextstep = (current[0]+i, current[1]+j)
            #... prevent from visiting again
            #See what happens if you disable this check here
            #if nextstep in self.checked or nextstep in self.frontier:
            #    print("expanded before: ", nextstep)
            #    continue
            #... check if it's in boundaries of the grid
            if 0 <= nextstep[0] < self.grid.row_range:
                if 0 <= nextstep[1] < self.grid.col_range:
                    #... check if puddle
                    if not self.grid.nodes[nextstep[0]][nextstep[1]].puddle:
                        if not nextstep in self.checked:
                            if nextstep == self.goal:
                                self.finished = True
                            next_cost = current_cost + self.grid.nodes[nextstep[0]][nextstep[1]].cost()
                            self.gdict[nextstep] = next_cost
                            #   the big difference vs just UCS is the heuristic value adding onto the cost
                            if not (next_cost + self.h_val(self.goal,nextstep), nextstep) in self.frontier:
                                #   also seen here
                                heappush(self.frontier, (next_cost + self.h_val(self.goal,nextstep), nextstep))
                                self.grid.nodes[nextstep[0]][nextstep[1]].frontier = True
                                self.came_from[nextstep] = current
                                print("pushed: ", nextstep)
                            else:
                                print("expanded before: ", nextstep)
                        else:
                            print("checked before: ", nextstep)
                    else:
                        print("puddle at: ", nextstep)
                else:
                    print("out of column range: ", nextstep)
            else:
                print("out of row range: ", nextstep)
