from MakeMove import MakeMove
from helperFunctions import make_graph,get_player_position,get_opponent_position,can_steal_koalas,check_cell

Api=MakeMove()

player,(d,matrix)=Api.MakeGame()
player=str(player+1)

print(player)

mv_str="edsaqw"
score={
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

	if False and can_steal_koalas(go,my_pos,opp_pos,player,d):
		print(d['player1']['x'],d['player1']['y'])
		print(d['player2']['x'],d['player2']['y'])
		d,matrix=Api.StealKoalas()
	else:
		best_mv=(-1,-1)
		best_delta=-10000000
		for i in range(6):
			dist=1
			delta_score=100
			dest=my_pos
			while True:
				dest=go[dest[0]][dest[1]][i]
				if dest==None or (not check_cell(dest,matrix)) or my_energy<dist:
					break
				delta_score-=100
				delta_score+=score[matrix[dest[0]][dest[1]]]
				if delta_score>best_delta:
					best_delta=delta_score
					best_mv=(i,dist)
				dist+=1
		if best_mv[0]==-1:
			d,matrix=Api.Move("w",1)
		else:
			d,matrix=Api.Move(mv_str[best_mv[0]],best_mv[1])
	if d['finished']==True:
		break
