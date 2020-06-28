import pickle
import numpy as np
import os.path as path

filename = path.join(path.dirname(__file__),"save/result.pickle")
with open(filename, 'rb') as file:
    model = pickle.load(file)

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
        car_right=[]
        car_left=[]
        car_front=[]
        player_x=0
        
        if scene_info[self.player] != () :
            player_x=scene_info[self.player][0]
            player_y=scene_info[self.player][1]
            player_v=scene_info["cars_info"][self.player_no]["velocity"] 
        
            for i in range(len(scene_info["cars_info"])): 
                if scene_info["cars_info"][i]["id"] != self.player_no :
                    car_x_temp=scene_info["cars_info"][i]["pos"][0]
                    car_y_temp=scene_info["cars_info"][i]["pos"][1]
                    car_v_temp=scene_info["cars_info"][i]["velocity"]

                    #電腦車子分前左右
                    if car_y_temp < player_y and abs(car_x_temp-player_x) <= 41 and car_y_temp > -40: #車子在前面
                        car_x_temp=car_x_temp-player_x
                        car_y_temp=player_y-car_y_temp
                        temp=(car_x_temp,car_y_temp,car_v_temp)
                        car_front.append(temp)
                    else :
                        if car_x_temp > player_x and car_x_temp-player_x < 71 : #車子在右邊
                            car_x_temp=car_x_temp-player_x
                            car_y_temp=car_y_temp-player_y
                            temp=(car_x_temp,car_y_temp)
                            car_right.append(temp)
                        elif car_x_temp < player_x and player_x-car_x_temp < 71 : #車子在左邊
                            car_x_temp=car_x_temp-player_x
                            car_y_temp=car_y_temp-player_y
                            temp=(car_x_temp,car_y_temp)
                            car_left.append(temp)
            
            #排前面的車子
            for t in range((len(car_front)-1),0,-1):
                for s in range(0,t):
                    if car_front[s][0] > car_front[s+1][0] :
                        car_front[s],car_front[s+1]=car_front[s+1],car_front[s]
            #排右邊的車子
            for t in range((len(car_right)-1),0,-1):
                for s in range(0,t):
                    if abs(car_right[s][1]) > abs(car_right[s+1][1]) :
                        car_right[s],car_right[s+1]=car_right[s+1],car_right[s]
            #排左邊的車子
            for t in range((len(car_left)-1),0,-1):
                for s in range(0,t):
                    if abs(car_left[s][1]) > abs(car_left[s+1][1]) :
                        car_left[s],car_left[s+1]=car_left[s+1],car_left[s]

            #寫資料
            if len(car_front) != 0 :
                front_x=car_front[0][0]
                front_y=car_front[0][1]
                front_v=car_front[0][2]
            
                if len(car_right) == 0 :
                    right_dis=1000
                    right_1=1000
                    right_2=1000
                elif len(car_right) == 1 :
                    right_dis=car_right[0][0]
                    right_1=car_right[0][1]
                    right_2=1000
                else :
                    right_dis=car_right[0][0]
                    right_1=car_right[0][1]
                    right_2=car_right[1][1]

                if len(car_left) == 0 :
                    left_dis=-1000
                    left_1=1000
                    left_2=1000
                elif len(car_left) == 1 :
                    left_dis=car_left[0][0]
                    left_1=car_left[0][1]
                    left_2=1000
                else :
                    left_dis=car_left[0][0]
                    left_1=car_left[0][1]
                    left_2=car_left[1][1]

                #player_x,player_v,right_dis,right_1,right_2,left_dis,left_1,left_2,front_x,front_y,front_v
                data=[player_x,player_v,right_dis,right_1,right_2,left_dis,left_1,left_2,front_x,front_y,front_v]
                data=np.array(data)
                result=model.predict([data])
                if (result == 3 or result == 5 or result == 7) and player_x > 595 :
                    result = 0
                if (result == 3 or result == 5 or result == 7) and (abs(right_1) < 90 or abs(right_2) < 90) :
                    result = 6
                if (result == 4 or result == 6 or result == 8) and (abs(left_1) < 90 or abs(left_2) < 90) :
                    result = 5
                if front_y < 140  and player_v > 10:
                    result = 2
            else :
                result = 1
        else :
            result = 0

        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        
        #command 
        #0:nothing 1:speed 2:break 3:right 4:left
        #5:speed right 6:speed left 7:break right 8:break left 
        if result == 0 :
            return []
        elif result == 1 :
            #35, 105, 175, 245, 315, 385, 455, 525, 595
            if (player_x < 25 and player_x > 20) or (player_x < 95 and player_x > 70) or (player_x < 165 and player_x > 140) or (player_x < 235 and player_x > 210) or (player_x < 305 and player_x > 280) or (player_x < 375 and player_x > 350) or (player_x < 445 and player_x > 420) or (player_x < 515 and player_x > 490) or (player_x < 585 and player_x > 560):
                return ["SPEED","MOVE_RIGHT"]
            if (player_x < 70 and player_x > 45) or (player_x < 140 and player_x > 115) or (player_x < 210 and player_x > 185) or (player_x < 280 and player_x > 255) or (player_x < 350 and player_x > 325) or (player_x < 420 and player_x > 395) or (player_x < 490 and player_x > 465) or (player_x < 560 and player_x > 535) or (player_x < 605 and player_x > 605):
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
