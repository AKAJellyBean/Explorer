import heapq

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, grid):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:  # 4 directions
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.cols and 0 <= ny < grid.rows:
            npos = (nx, ny)
            if (npos not in grid.lake_pos and
                npos not in grid.decor_pos and
                npos not in grid.sheltor_pos):
                neighbors.append(npos)
    return neighbors

def a_star(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # No path found
