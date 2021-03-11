from MakeMove import MakeMove
from helperFunctions import make_graph,get_player_position,get_opponent_position,can_steal_koalas,check_cell

Api=MakeMove()

player,(d,matrix)=Api.MakeGame()
player=str(player+1)

print(player)

mv_str="edsaqw"
score_of={
	"0": 0,
	"k": 150,
	"e": 100,
	"kc": 1500,
	"f": 700,
}

while True:
	go=make_graph(matrix)
	my_pos=get_player_position(matrix,player)
	my_energy=d['player'+player]['energy']
	opp_pos=get_opponent_position(matrix,player)

	print(d['player1']['score'],"-",d['player2']['score'])

	if can_steal_koalas(go,my_pos,opp_pos,player,d):
		print(d['player1']['x'],d['player1']['y'])
		print(d['player2']['x'],d['player2']['y'])
		d,matrix=Api.StealKoalas()
	else:
		def rec_to_depth(pos,energy,matrix,depth=10):
			if depth==0:
				return 0,(-1,-1)
			best_mv=(-1,-1)
			best_delta=-500
			for i in range(6):
				dist=1
				delta_score=100
				e_cnt=0
				dest=pos
				saved=[matrix[pos[0]][pos[1]]]
				matrix[pos[0]][pos[1]]='b'+player
				while True:
					pre=dest
					dest=go[dest[0]][dest[1]][i]
					if dest==None or (not check_cell(dest,matrix)) or my_energy<dist:
						break
					delta_score-=100
					delta_score+=score_of[matrix[dest[0]][dest[1]]]
					if matrix[dest[0]][dest[1]]=='e':
						e_cnt+=1
					saved.append(matrix[dest[0]][dest[1]])
					if dist!=1:
						matrix[pre[0]][pre[1]]='0'
					matrix[dest[0]][dest[1]]=player
					score=delta_score+rec_to_depth(dest,energy-dist+e_cnt,matrix,depth-1)[0]
					if score>best_delta:
						best_delta=score
						best_mv=(i,dist)
					dist+=1
				j=0
				dest=pos
				while dist>0:
					matrix[dest[0]][dest[1]]=saved[j]
					j+=1
					dist-=1
			return best_delta,best_mv
		best_delta,best_mv=rec_to_depth(my_pos,my_energy,matrix)
		'''
		best_mv=(-1,-1)
		best_delta=-10000000
		for i in range(6):
			dist=1
			delta_score=100
			while True:
				dest=go[my_pos[0]][my_pos[1]][i]
				if dest==None or (not check_cell(dest,matrix)) or my_energy<dist:
					break
				delta_score-=100
				delta_score+=score[matrix[dest[0]][dest[1]]]
				if delta_score>best_delta:
					best_delta=delta_score
					best_mv=(i,dist)
				dist+=1
		'''
		if best_mv[0]==-1:
			d,matrix=Api.Move("w",1)
		else:
			d,matrix=Api.Move(mv_str[best_mv[0]],best_mv[1])
	if d['finished']==True:
		break
