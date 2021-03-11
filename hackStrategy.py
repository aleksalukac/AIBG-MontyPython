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

turns_skipped=0

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
		has_good_move=False
		invalid_move=-1
		for i in range(6):
			dest=go[my_pos[0]][my_pos[1]][i]
			if dest==None or (not check_cell(dest,matrix)):
				invalid_move=i
			else:
				for j in range(6):
					nxt=go[dest[0]][dest[1]][j]
					if nxt!=None and check_cell(nxt,matrix):
						has_good_move=True

		if has_good_move:
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
		else:
			if turns_skipped<5:
				turns_skipped+=1
				d,matrix=Api.SkipATurn()
			else:
				d,matrix=Api.Move(mv_str[invalid_move],1)
	if d['finished']==True:
		break
