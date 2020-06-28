import pickle
import numpy as np
import os.path as path
import math

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        self.coin_num = 0
        self.computer_cars = []
        self.coins_pos = []
    
    def update(self, scene_info):
        row=[list() for i in range(9)]
        player_x=0
        player_y=0
        player_v=0
        player_row=0
        result = 1

        def checkrow(x):
            if x > 0 and x <= 70:
                return 1
            elif x > 70 and x <= 140:
                return 2
            elif x > 140 and x <= 210:
                return 3
            elif x > 210 and x <= 280:
                return 4
            elif x > 280 and x <= 350:
                return 5
            elif x > 350 and x <= 420:
                return 6
            elif x > 420 and x <= 490:
                return 7
            elif x > 490 and x <= 560:
                return 8
            elif x > 560 and x <= 630:
                return 9

        name = path.join(path.dirname(__file__),'save/record.txt')
        f=open(name,'r')
        record=f.read()
        f.close()
        record=int(record)
        
        if scene_info[self.player] != () :
            player_x=scene_info[self.player][0]
            player_y=scene_info[self.player][1]
            player_v=scene_info["cars_info"][self.player_no]["velocity"]
            player_row=checkrow(player_x) 
        
            for i in range(len(scene_info["cars_info"])): 
                if scene_info["cars_info"][i]["id"] != self.player_no :
                    car_x_temp=scene_info["cars_info"][i]["pos"][0]
                    car_y_temp=scene_info["cars_info"][i]["pos"][1]
                    car_v_temp=scene_info["cars_info"][i]["velocity"]
                    car_row_temp=checkrow(car_x_temp)
                    temp=(car_x_temp,car_y_temp,car_v_temp)

                    #車子分排
                    #35, 105, 175, 245, 315, 385, 455, 525, 595
                    if car_row_temp == 1:
                        row[0].append(temp)
                    elif car_row_temp == 2:
                        row[1].append(temp)
                    elif car_row_temp == 3:
                        row[2].append(temp)
                    elif car_row_temp == 4:
                        row[3].append(temp)
                    elif car_row_temp == 5:
                        row[4].append(temp)
                    elif car_row_temp == 6:
                        row[5].append(temp)
                    elif car_row_temp == 7:
                        row[6].append(temp)
                    elif car_row_temp == 8:
                        row[7].append(temp)
                    elif car_row_temp == 9:
                        row[8].append(temp)
            #9宮格
            block1=[1000,1000,0]#左最近
            block2=[1000,1000,0]#前最近
            block3=[1000,1000,0]#右最近
            #block4=[1000,1000,0]#左第二近
            #block5=[1000,1000,0]#右第二近
            if row[player_row-1] != []:
                for i in range(len(row[player_row-1])):
                    if abs(player_y-row[player_row-1][i][1]) < abs(player_y-block2[1]) and player_y > row[player_row-1][i][1]:
                        block2=row[player_row-1][i]
            if player_row-2 > -1:
                if row[player_row-2] != []:
                    for i in range(len(row[player_row-2])):
                        if abs(player_y-row[player_row-2][i][1]) < abs(player_y-block1[1]):
                            block1=row[player_row-2][i]
            if player_row < 9:
                if row[player_row] != []:
                    for i in range(len(row[player_row])):
                        if abs(player_y-row[player_row][i][1]) < abs(player_y-block3[1]):
                            block3=row[player_row][i]
            '''if player_row-2 > -1:
                if len(row[player_row-2]) > 1:
                    for i in range(len(row[player_row-2])):
                        if abs(player_y-row[player_row-2][i][1]) < block4[1] and row[player_row-2] != block1:
                            block4=row[player_row-2][i]
            if player_row < 9:
                if len(row[player_row]) > 1:
                    for i in range(len(row[player_row])):
                        if abs(player_y-row[player_row][i][1]) < block5[1] and row[player_row] != block3:
                            block5=row[player_row][i]'''
            
            
            #條件判斷
            if block2[1] == 1000 or player_y-block2[1]>200:
                print("coin")
                coin=[10000,10000]
                #吃COIN機制
                for i in range(len(scene_info["coins"])):
                    coin_x=abs(scene_info["coins"][i][0]-player_x)
                    coin_y=abs(scene_info["coins"][i][1]-player_y)
                    coin_x_temp=abs(coin[0]-player_x)
                    coin_y_temp=abs(coin[1]-player_y)
                    coin_row=checkrow(scene_info["coins"][i][0])
                    if math.sqrt(coin_x**2+coin_y**2) < math.sqrt(coin_x_temp**2+coin_y_temp**2) and scene_info["coins"][i][1] < player_y and abs(coin_row-player_row) < 3:
                        coin=scene_info["coins"][i]
                if coin[0] == 10000:
                    result = 1
                else:
                    coin_row=checkrow(coin[0])
                    if coin_row-player_row > 0 and ((abs(player_y-block3[1]) > 60 and player_y < block3[1]) or (abs(player_y-block3[1]) > 200 and player_y > block3[1])) and player_row != 9:
                        result = 5
                    elif coin_row-player_row < 0 and ((abs(player_y-block1[1]) > 60 and player_y < block1[1]) or (abs(player_y-block1[1]) > 200 and player_y > block1[1])) and player_row != 1:
                        result = 6
                    else:
                        result = 1
            else:
                print("rule")
                if ((abs(player_y-block3[1]) > 80 and player_y < block3[1]) or (abs(player_y-block3[1]) > 270 and player_y > block3[1])) and player_row != 9:
                   result = 5 
                elif ((abs(player_y-block1[1]) > 80 and player_y < block1[1]) or (abs(player_y-block1[1]) > 270 and player_y > block1[1])) and player_row != 1:
                    result = 6
                else:
                    result = 0
            if abs(player_y-block2[1]) < 140:
                result = 0 
            if abs(player_y-block2[1]) < 120:
                if ((abs(player_y-block3[1]) > 130 and player_y < block3[1]) or (abs(player_y-block3[1]) > 130 and player_y > block3[1])) and player_row != 9:
                   result = 7 
                elif ((abs(player_y-block1[1]) > 130 and player_y < block1[1]) or (abs(player_y-block1[1]) > 130 and player_y > block1[1])) and player_row != 1:
                    result = 8
                else:
                    result = 2 
        else :
            result = 0

        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"] == self.player_no:
                self.car_vel = car["velocity"]
                self.coin_num = car["coin_num"]
        self.computer_cars = scene_info["computer_cars"]
        if scene_info.__contains__("coins"):
            self.coins_pos = scene_info["coins"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        
        #command 
        #0:nothing 1:speed 2:break 3:right 4:left
        #5:speed right 6:speed left 7:break right 8:break left

        record = result
        record=str(record)
        f = open(name, 'w')
        f.write(record)
        f.close()
        print(result)
        if result == 0 :
            return []
        elif result == 1 :
            if (player_x < 31 and player_x > 20) or (player_x < 101 and player_x > 70) or (player_x < 171 and player_x > 140) or (player_x < 241 and player_x > 210) or (player_x < 311 and player_x > 280) or (player_x < 381 and player_x > 350) or (player_x < 451 and player_x > 420) or (player_x < 521 and player_x > 490) or (player_x < 591 and player_x > 560):
                return ["SPEED","MOVE_RIGHT"]
            if (player_x <= 70 and player_x > 38) or (player_x <= 140 and player_x > 108) or (player_x <= 210 and player_x > 178) or (player_x <= 280 and player_x > 248) or (player_x <= 350 and player_x > 318) or (player_x <= 420 and player_x > 388) or (player_x <= 490 and player_x > 458) or (player_x <= 560 and player_x > 528) or (player_x <= 605 and player_x > 598):
                return ["SPEED","MOVE_LEFT"]
            else :
                return ["SPEED"]              
        elif result == 2 :
            return ["BRAKE"]
        elif result == 3 :
            return ["MOVE_RIGHT"]
        elif result == 4 :
            return ["MOVE_LEFT"]
        elif result == 5 :
            return ["SPEED","MOVE_RIGHT"]
        elif result == 6 :
            return ["SPEED","MOVE_LEFT"]
        elif result == 7 :
            return ["BRAKE","MOVE_RIGHT"]
        elif result == 8:
            return ["BRAKE","MOVE_LEFT"]
        else :
            return ["SPEED"]
        
        
    def reset(self):
        pass