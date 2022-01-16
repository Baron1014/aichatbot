import numpy as np
from linebot.models import TextSendMessage

def get_map():
    uimap = np.empty((8, 8), dtype=object)

    # init
    for i in range(uimap.shape[0]):
        for j in range(uimap.shape[1]):
            if i==7 and j==3:
                uimap[i, j] = "D"
            elif i==5 and j==3:
                uimap[i, j] = "P"
            elif i==5 and j==2:
                uimap[i, j] = "C"
            else:
                uimap[i,j] = "B"

    uimap, _ = set_player(uimap, 6, 3)

    # numpy to string
    for i in range(uimap.shape[0]):
        if i ==0:
            s = "".join(uimap[i].tolist())
        else:
            s = s + "\n" + "".join(uimap[i].tolist())

    response = TextSendMessage(text=set_icon(s))

    return response, s

def set_player(uimap, x, y):
    for xx in range(x-1, x+2):
        for yy in range(y-1, y+2):
            # 若想要設置的地方有雞或豬則跳過此次設置，並返回錯誤訊息
            setting_error_str=False
            if uimap[x ,y] == "C":
                setting_error_str = "小雞似乎擋住了你的去路，試著走其他路線吧！"
            elif uimap[x ,y] == "P":
                setting_error_str = "兇猛的野豬使你不敢靠近他，試著走其他路線吧！"
            elif uimap[x ,y] == "T":
                setting_error_str = "寶箱上有著一個大鎖，密碼似乎在房間裡的某個地方..."
            if setting_error_str:
                return None, setting_error_str

            # 正常移動
            if xx==x and yy==y:
                uimap[xx,yy] = "U"
                continue
            # wall
            if xx==uimap.shape[0]-1 or xx==0:
                if uimap[xx,yy] != "D":
                    uimap[xx,yy] = "W"
            if yy==uimap.shape[1]-1 or yy==0:
                uimap[xx,yy] = "W"
            # 符合條件為謎題
            if xx==3 and yy==7:
                uimap[xx,yy] = "Q"
            
            #判斷影子地應該出現何物
            if uimap[xx,yy] == "B":
                # 是否出現寶箱
                if xx==2 and yy==2:
                    uimap[xx, yy] = "T"
                else:
                    uimap[xx,yy] = "N"
            # 移除舊的player
            if uimap[xx, yy]=="U":
                uimap[xx, yy] = "N"
    
    return uimap, None

def update_player(map_str, orientation):
    re = list()
    # player old location
    old_location = map_str.find("U")
    old_row = old_location // 9 
    old_col = old_location % 9
    
    # init warring state
    warr = False

    # string to numpy array
    one_split = map_str.split("\n")
    two_split = [list(row) for row in one_split]
    if orientation=="右":
        if old_col+1 ==7:
            warr=True
        else:
            map_array, setting_error = set_player(np.array(two_split), old_row, old_col+1)
    elif orientation=="左":
        if old_col-1 <=0:
            warr=True
        else:
            map_array, setting_error = set_player(np.array(two_split), old_row, old_col-1)
    elif orientation=="上":
        if old_row-1 <=0:
            warr=True
        else:
            map_array, setting_error = set_player(np.array(two_split), old_row-1, old_col)
    elif orientation=="下":
        if old_row+1 ==7:
            warr=True
        else:
            map_array, setting_error = set_player(np.array(two_split), old_row+1, old_col)

    # 若不能移動則跳出警告訊息
    if warr:
        s = map_str
        if old_row==3 and old_col==6:
            re_str = "畫上似乎描述著什麼，好像有一些線索..."
        elif old_row==6 and old_col==3:
            re_str = "骨瘦如柴的你，用盡全力也無法推開這個上鎖的門"
        else:
            re_str = orientation+"方是一面牆壁，似乎沒有辦法繼續往前移動"
    else:
        # 設定新玩家位置時出錯
        if setting_error:
            s = map_str
            re_str = setting_error
        else:
            # numpy to string
            for i in range(map_array.shape[0]):
                if i ==0:
                    s = "".join(map_array[i].tolist())
                else:
                    s = s + "\n" + "".join(map_array[i].tolist())
            re_str = "你向"+orientation+"移動一格"

    re.append(TextSendMessage(text=set_icon(s)))
    re.append(TextSendMessage(text=re_str))

    return re, s, re_str

def set_icon(map_string):
    player = "🤠"
    chicken = "🐤"
    pig = "🐗"
    painting = "🖼"
    treasure = "🎁"
    door = "🚪"
    wall = "🟫"
    black = "⬛️"
    nothing = "⬜️"
    meat = "🍖"

    # replace string to icon
    map_string = map_string.replace("B", black)
    map_string = map_string.replace("C", chicken)
    map_string = map_string.replace("P", pig)
    map_string = map_string.replace("D", door)
    map_string = map_string.replace("W", wall)
    map_string = map_string.replace("N", nothing)
    map_string = map_string.replace("U", player)
    map_string = map_string.replace("Q", painting)
    map_string = map_string.replace("T", treasure)
    map_string = map_string.replace("M", meat)

    return map_string


if __name__=="__main__":
    m = get_map()
    # s1 = "".join(m[0].tolist())
    # s2 = "".join(m[1].tolist())
    # print(s1+"\n"+s2)
    