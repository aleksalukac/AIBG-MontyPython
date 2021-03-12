from MakeMove import MakeMove
from helperFunctions import make_graph,get_player_position,get_opponent_position,can_steal_koalas,check_cell

Api=MakeMove()

player,(d,matrix)=Api.MakeGame()
player=str(player+1)

print(player)

mv_str="edsaqw"

while True:
	go=make_graph(matrix)
	my_pos=get_player_position(matrix,player)
	opp_pos=get_opponent_position(matrix,player)

	print(d['player1']['score'],"-",d['player2']['score'])

	if can_steal_koalas(go,my_pos,opp_pos,player,d):
		print(d['player1']['x'],d['player1']['y'])
		print(d['player2']['x'],d['player2']['y'])
		d,matrix=Api.StealKoalas()
	else:
		mv=-1
		for i in range(6):
			dest=go[my_pos[0]][my_pos[1]][i]
			if dest!=None and check_cell(dest,matrix):
				mv=i
				break
		if mv==-1:
			d,matrix=Api.Move("w",1)
		else:
			d,matrix=Api.Move(mv_str[mv],1)
	if d['finished']==True:
		break
