
def make_graph(matrix):
	go=[[[None for _ in range(6)] for _ in range(9)] for _ in range(27)]
	for i in range(1,27,2):
		for j in range(8):
			if i>1 and matrix[i][j]!="h" and matrix[i-2][j]!="h":
				go[i][j][5]=(i-2,j)
				go[i-2][j][2]=(i,j)
			if matrix[i][j]!="h" and matrix[i-1][j]!="h":
				go[i][j][4]=(i-1,j)
				go[i-1][j][1]=(i,j)
			if matrix[i][j]!="h" and matrix[i-1][j+1]!="h":
				go[i][j][0]=(i-1,j+1)
				go[i-1][j+1][3]=(i,j)
			if matrix[i][j]!="h" and matrix[i+1][j]!="h":
				go[i][j][3]=(i+1,j)
				go[i+1][j][0]=(i,j)
			if matrix[i][j]!="h" and matrix[i+1][j+1]!="h":
				go[i][j][1]=(i+1,j+1)
				go[i+1][j+1][4]=(i,j)
	for i in range(2,27,2):
		for j in range(9):
			if matrix[i][j]!="h" and matrix[i-2][j]!="h":
				go[i][j][5]=(i-2,j)
				go[i-2][j][2]=(i,j)
	return go

def get_player_position(matrix,player):
	for i in range(27):
		for j in range(9):
			if matrix[i][j]==player:
				return (i,j)
	return None

def get_opponent_position(matrix,player):
	for i in range(27):
		for j in range(9):
			if matrix[i][j]!=player and (matrix[i][j] in ['1','2']):
				return (i,j)
	return None

def can_steal_koalas(go,my_pos,opp_pos,player,d):
	if d['player'+player]['energy']<5:
		return False
	for i in range(6):
		if go[my_pos[0]][my_pos[1]][i]==opp_pos:
			return True
	return False

def check_cell(pos,matrix):
	return matrix[pos[0]][pos[1]] in ["0","e","k","kc","f"]

def find_distances(go,matrix,my_pos):
	dist=[[-1 for _ in range(9)] for _ in range(27)]
	q=[0 for _ in range(27*9)]
	ql=qr=0
	dist[my_pos[0]][my_pos[1]]=0
	q[qr]=my_pos
	qr+=1
	while ql<qr:
		u=q[ql]
		ql+=1
		for i in range(6):
			v=go[u][i]
			if v!=None and dist[v[0]][v[1]]==-1 and check_cell(v,matrix):
				dist[v[0]][v[1]]=dist[u[0]][u[1]]+1
				q[qr]=v
				qr+=1
	return dist
