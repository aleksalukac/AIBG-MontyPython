from MakeMove import MakeMove
from helperFunctions import make_graph,get_player_position,get_opponent_position,can_steal_koalas,check_cell

Api=MakeMove('MontyPython 2',677,665338)

#player,(d,matrix)=Api.JoinGame()
player,(d,matrix) = Api.MakeGame()
#matrix[0][1] = 'f'
player=str(player+1)

print(player)

mv_str="edsaqw"
score_of={
	"0": 0,
	"k": 150,
	"e": 100,
	"kc": 1500,
	"f": 2000,
}

turns_skipped=0

while True:
	#matrix[0][1] = 'f'
	go=make_graph(matrix)
	my_pos=get_player_position(matrix,player)
	my_energy=d['player'+player]['energy']
	opp_pos=get_opponent_position(matrix,player)

	print(d['player1']['score'],"-",d['player2']['score'])

	if can_steal_koalas(go,my_pos,opp_pos,player,d):
		print(d['player1']['x'],d['player1']['y'])
		print(d['player2']['x'],d['player2']['y'])
		if(d['player' + str(3 - int(player))]['gatheredKoalas'] >= 2):
			d,matrix = Api.StealKoalas()
			continue

	good_mv=(-1,-1)
	good_mv2 = (-1,-1)
	for i in range(6):
		dist=1
		dest=my_pos
		while True:
			dest=go[dest[0]][dest[1]][i]
			if dest==None or (not check_cell(dest,matrix)) or my_energy<dist:
				break
			if matrix[dest[0]][dest[1]] in ['f','kc']:
				good_mv=(i,dist)
				print("****************IMA GM1*************")

			for j in range(6):
				dist2=1
				dest2=dest
 
				while True:
					dest2=go[dest2[0]][dest2[1]][j]
					if dest2==None or (not check_cell(dest2,matrix)) or my_energy + 1<dist + dist2:
						break
					if matrix[dest2[0]][dest2[1]] in ['f','kc']:
						good_mv2=(i,dist)
						print("****************IMA GM2*************")
						
					dist2+=1
			dist+=1
	if good_mv[0]!=-1:
		d,matrix=Api.Move(mv_str[good_mv[0]],good_mv[1])
	elif good_mv2[0] != -1:
		d,matrix = Api.Move(mv_str[good_mv2[0]], good_mv2[1])

	else:
		def dfs(u,was):
			was[u[0]][u[1]]=True
			ans=1
			for i in range(6):
				v=go[u[0]][u[1]][i]
				if v==None or was[v[0]][v[1]] or (not check_cell(v,matrix)):
					continue
				ans+=dfs(v,was)
			return ans

		was=[[False for _ in range(9)] for _ in range(27)]
		cmp_sz=dfs(my_pos,was)
		good_ind=-1
		for i in range(6):
			u=go[my_pos[0]][my_pos[1]][i]
			if u==None or not was[u[0]][u[1]]:
				continue
			u=go[u[0]][u[1]][i]
			if u==None or not was[u[0]][u[1]]:
				continue
			u=go[u[0]][u[1]][i]
			if u==None or not was[u[0]][u[1]]:
				continue
			good_ind=i
		if cmp_sz==4 and good_ind!=-1 and my_energy>1:
			d,matrix=Api.Move(mv_str[good_ind],2)
		else:

			has_good_move=False
			invalid_move=-1
			for i in range(6):
				dest=go[my_pos[0]][my_pos[1]][i]
				if dest==None or (not check_cell(dest,matrix)):
					invalid_move=i
				else:
					good=False
					lose_koalas=False
					for j in range(6):
						nxt=go[dest[0]][dest[1]][j]
						if nxt!=None and check_cell(nxt,matrix):
							good=True
						if nxt!=None and (matrix[nxt[0]][nxt[1]] in ['1','2'] and matrix[nxt[0]][nxt[1]]!=player):
							lose_koalas=True
					if (not lose_koalas) and good:
						has_good_move=True

			if has_good_move:
				def koala_trap(u,matrix):
					cnt=0
					bad=False
					for i in range(6):
						v=go[u[0]][u[1]][i]
						if v==None or (not check_cell(v,matrix)):
							continue
						cnt+=1
						for j in range(6):
							w=go[v[0]][v[1]][j]
							if w!=None and check_cell(w,matrix):
								bad=True
					return (not bad) and cnt>1

				def rec_to_depth(pos,energy,matrix):
					best_mv=(-1,-1)
					best_delta=-500
					if koala_trap(pos,matrix):
						best_delta=4000
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
							score=delta_score+rec_to_depth(dest,energy-dist+e_cnt,matrix)[0]
							if score>=best_delta:
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
				if best_mv[0]==-1:
					d,matrix=Api.Move("w",1)
				else:
					d,matrix=Api.Move(mv_str[best_mv[0]],best_mv[1])
			else:
				br=(-1,-1)
				cnt=0
				for i in range(6):
					dest=go[my_pos[0]][my_pos[1]][i]
					if dest!=None and check_cell(dest,matrix):
						cnt+=1
					if dest==None or matrix[dest[0]][dest[1]] not in ['b1', 'b2']:
						continue
					if matrix[dest[0]][dest[1]]!='b'+player:
						br=dest
					elif br[0]==-1:
						br=dest
				if d['player'+player]['hasFreeASpot'] and cnt==1 and br[0]!=-1:
					d,matrix=Api.FreeASpot(br[0],br[1])
				elif turns_skipped<5:
					turns_skipped+=1
					d,matrix=Api.SkipATurn()
				else:
					d,matrix=Api.Move(mv_str[invalid_move],1)
	if d['finished']==True:
		break
