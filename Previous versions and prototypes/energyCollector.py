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
		invalid_move=0
		for i in range(6):
			dest=go[my_pos[0]][my_pos[1]][i]
			if dest==None or (not check_cell(dest,matrix)):
				invalid_move=i
		if turns_skipped<5:
			turns_skipped+=1
			d,matrix=Api.SkipATurn()
		else:
			d,matrix=Api.Move(mv_str[invalid_move],1)
	if d['finished']==True:
		break
