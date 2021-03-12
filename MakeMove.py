# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 18:25:21 2021

@author: Aleksa
"""
import requests 
from pathlib import Path
import json 
import os

# %%

class MakeMove():
    
    def __init__(self, name = 'MontyPython', gameId = -1, playerId = 665337):
        self.gameId = gameId
        self.name = name
        self.playerId = playerId
        p = Path(__file__).with_name('api.txt')
        
        with p.open('r') as f:
            self.api_endpoint = f.read()

        self.data=None
        self.matrix=None
            
    def JoinGame(self):
        url = self.api_endpoint+"joinGame?"
        url += "playerId=" + str(self.playerId)
        url += "&gameId=" + str(self.gameId)
        
        r = requests.get(url = url)
        print(r.url)
        
        data = json.loads(r.text)
        #print(r.text)
        
        #self.gameId = data['gameId']
        
        matrix = []
        
        self.player = 0 
        if(data['player2']['teamName'] == self.name):
            self.player = 1
        
        return self.player, self.ReturnMatrixAndData(data)
        
    def MakeGame(self):
        self.api_endpoint += "train/"
        url = self.api_endpoint + "makeGame?"
        url += "playerId=" + str(self.playerId)
        #url += "&gameId=" + str(self.gameId)

        r = requests.get(url=url)

        data = json.loads(r.text)
        #print(r.text)
        
        self.gameId = data['gameId']
        
        matrix = []
        
        self.player = 0 
        if(data['player2']['teamName'] == self.name):
            self.player = 1
        
        return self.player, self.ReturnMatrixAndData(data)
            
    def Move(self, direction, distance):
        '''data = {'playerId' : playerId,
                'gameId' : gameId,
                'direction' : direction,
                'distance' : distance}'''
        
        url = self.api_endpoint + "move?"
        url += "playerId=" + str(self.playerId)
        url += "&gameId=" + str(self.gameId)
        url += "&direction=" + direction
        url += "&distance=" + str(distance)
        
        r = requests.get(url = url)
        print(r.url)
        
        data = json.loads(r.text)
        #print(r.text)
        
        return self.ReturnMatrixAndData(data)
        
    def SkipATurn(self):
        url = self.api_endpoint + "skipATurn?"
        url += "playerId=" + str(self.playerId)
        url += "&gameId=" + str(self.gameId)
        
        r = requests.get(url = url)
        print(r.url)
        
        data = json.loads(r.text)
        #print(r.text)
        
        return self.ReturnMatrixAndData(data)
        
    def StealKoalas(self):
        url = self.api_endpoint + "stealKoalas?"
        #url = self.api_endpoint.replace('/train','') + "stealKoalas?"
        url += "playerId=" + str(self.playerId)
        url += "&gameId=" + str(self.gameId)
        
        r = requests.get(url = url)
        print(r.url)
        
        data = json.loads(r.text)
        #print(r.text)
        
        return self.ReturnMatrixAndData(data)
        
    def FreeASpot(self, x, y):
        url = self.api_endpoint + "freeASpot?"
        url += "playerId=" + str(self.playerId)
        url += "&gameId=" + str(self.gameId)
        url += "&&x=" + str(x)
        url += "&&y=" + str(y)
        
        r = requests.get(url = url)
        print(r.url)
        
        data = json.loads(r.text)
        #print(r.text)
        
        return self.ReturnMatrixAndData(data)
        
    def ReturnMatrixAndData(self, data):
        if 'map' not in data:
            print(data)
            return self.data,self.matrix
        tiles = data['map']['tiles']
        
        matrix = [[0 for x in range(9)] for y in range(27)]
        
        for i in range(27):
            for j in range(9):
                tile = tiles[i][j]
                
                if(tile['tileContent']['itemType'] == 'EMPTY'):
                    if(tile['ownedByTeam'] == self.name):
                        matrix[i][j] = 'b1'
                    elif(tile['ownedByTeam'] == ''):
                        matrix[i][j] = '0'
                    else:
                        matrix[i][j] = 'b2'
                
                if(tile['tileContent']['itemType'] == 'KOALA'):
                    matrix[i][j] = 'k'
                
                if(tile['tileContent']['itemType'] == 'HOLE'):
                    matrix[i][j] = 'h'
                    
                if(tile['tileContent']['itemType'] == 'ENERGY'):
                    matrix[i][j] = 'e'

                if(tile['tileContent']['itemType'] == 'KOALA_CREW'):
                    matrix[i][j] = 'kc'
                
                if(tile['tileContent']['itemType'] == 'FREE_A_SPOT'):
                    matrix[i][j] = 'f'
                    
        player1 = data['player1']
        matrix[player1['x']][player1['y']] = '1'
        
        player2 = data['player2']
        matrix[player2['x']][player2['y']] = '2'

        self.data=data
        self.matrix=matrix
        
        return data, matrix

"""
0 - empty
1 - player1
2 - player2
k - koala
e - energy
b1 - brick 1
b2 - brick 2
kc - koala crew
h - hole
f - free a spot
"""
    
'''
#%%
c = MakeMove(30)
c.MakeGame()

#%%
c.Move('w', 2)
c.SkipATurn()
sss = c.StealKoalas()
print(c.FreeASpot(2,3))
    
    
#%%
url = "https://aibg2021.herokuapp.com/train/" + "makeGame?"
url += "playerId=" + str(665337)

r = requests.get(url = url)
print(r.url)

data = json.loads(r.text)
print(r.text)


# %%

c = MakeMove()
player,_ = c.MakeGame()
d, matrix = c.Move('d', 1)
    
# %%

d, matrix = c.Move('e', 1)

d, matrix = c.Move('d', 1)

d, matrix = c.Move('e', 1)

d, matrix = c.Move('d', 1)
    
'''
    
    