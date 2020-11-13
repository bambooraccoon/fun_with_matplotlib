#Original code from https://scipython.com/blog/the-trapped-knight/

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
import sys

#DPI = 72
#width, height = 700, 525
#fig, ax = plt.subplots(figsize=(width/DPI, height/DPI), dpi=DPI)
fig, ax = plt.subplots()
ax.axis('square')

n = 200
grid = [[0]*n for i in range(n)]
ix, iy = 0, 0
dx, dy = 1, 0
s = 1
i = 0
while i <= n*n:
	for j in range(s):
		i += 1
		try:
			grid[iy+n//2][ix+n//2] = i
		except IndexError:
			break
		ix += dx
		iy += dy
	dx, dy = dy, dx
	if dy:
		dy = -dy
	else:
		s += 1

def get_next(iy, ix, my, mx):
	"""Get the position of the next square visited by the knight."""

	next_sq = []
	moves = (-mx,-my), (-mx,my), (mx,-my), (mx, my), (-my,-mx), (-my,mx), (my,-mx), (my,mx)
	for dy, dx in moves:
		jy, jx = iy + dy, ix + dx
		if 0 <= jx < n and 0 <= jy < n:
			if (jy, jx) not in visited:
				next_sq.append((jy, jx))
	if not next_sq:
		return
	return min(next_sq, key=lambda e: grid[e[0]][e[1]])

# Keep track of the visited squares' indexes in the list visited.
visited = []
my, mx = 1, 2
if len(sys.argv) > 2:
	my = int(sys.argv[1])
	mx = int(sys.argv[2])
print("{}x{} knight trying to escape".format(my, mx))
iy, ix = n//2, n//2
i = 0
# Run the game until there are no valid moves and print the visited squares.
while True:
	i += 1
	visited.append((iy, ix))
	try:
		iy, ix = get_next(iy, ix, my, mx)
	except TypeError:
		break
print(', '.join(str(grid[iy][ix]) for iy, ix in visited))
print('Done in {} steps'.format(i))

# Plot the path of the knight on a chessboard in a pleasing colour scheme.
points = np.array(visited).reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
norm = plt.Normalize(1, len(visited))
lc = LineCollection(segments, cmap='plasma_r', norm=norm)
lc.set_array(np.array(range(len(visited))))
# line = ax.add_collection(lc)

ax.scatter([visited[0][0]], [visited[0][1]], c=('g'), marker='*', zorder=10)
ax.scatter([visited[-1][0]], [visited[-1][1]], c=('r'), marker='*', zorder=10)

ptp = np.concatenate( (np.min(points[:,:], axis=0),
					   np.max(points[:,:], axis=0)) ).T

ax.set_xlim(ptp[0][0]-0.5, ptp[0][1]+0.5)
ax.set_ylim(ptp[1][0]-0.5, ptp[1][1]+0.5)

xmin, xmax = ptp[0]
ymin, ymax = ptp[1]
board = np.zeros((ymax-ymin+1, xmax-xmin+1), dtype=int)
board[1::2, ::2] = 1
board[::2, 1::2] = 1

cmap = ListedColormap(['#aaaaaa', 'white'])

ax.imshow(board, extent=[xmin-0.5,xmax+0.5,ymin-0.5,ymax+0.5], cmap=cmap)
plt.title('Trapped {}x{} Knight in {} Steps'.format(mx, my, i))

plt.savefig('trapped_knight_{}x{}.png'.format(mx, my))

total_frames = 200
steps_per_frame = i // total_frames

line, = ax.plot([],[])

def init():
	line.set_data([], [])
	return line,

def animate(i):
	if i < total_frames:
		lc = LineCollection(segments[:i*steps_per_frame], cmap='plasma_r', norm=norm)
	else:
		lc = LineCollection(segments, cmap='plasma_r', norm=norm)

	lc.set_array(np.array(range(len(visited))))
	line = ax.add_collection(lc)
	return line,

anim = FuncAnimation(fig, animate, init_func=init, frames=total_frames+(total_frames//20), interval=1, blit=True)
#anim.save('trapped_knight.gif', writer='imagemagick')

plt.show()

