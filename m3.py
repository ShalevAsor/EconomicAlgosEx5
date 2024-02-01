from typing import List

#Q_2
# def weighted_round_robin(rights: list[float],valuations: list[list[float]],y: float):
#     items = len(valuations[0])
#     players = len(rights)
#     curr_partition = [0]*players
#     item_index = 1
#     quotients = [(0, 0)] * players
#     while items > 0:
#
#         for i in range(players):
#             quotients[i] = (i, rights[i]/f(curr_partition[i],y))
#         quotients_tmp = quotients
#         quotients_tmp.sort()
#         player_index = quotients_tmp[0][0]
#         curr_partition[player_index] += 1
#         print("player "+ str(player_index) +" takes item: " + str(item_index) + "with value: " +str(valuations[player_index][item_index-1]))
#         items -= 1
#         item_index += 1

def weighted_round_robin(rights: list[float], valuations: list[list[float]], y: float):
    items = len(valuations[0])
    players = len(rights)
    curr_partition = [0] * players
    item_index = 1

    while items > 0:
        quotients = [(i, rights[i] / f(curr_partition[i] , y)) for i in range(players)]
        quotients_tmp = sorted(quotients, key=lambda x: x[1])
        player_index = quotients_tmp[0][0]

        curr_partition[player_index] += 1
        print("Player " + str(player_index) + " takes item " + str(item_index) +
              " with value " + str(valuations[player_index][item_index - 1]))

        items -= 1
        item_index += 1








def f(s: float,y: float) -> float:
    return s+y

if __name__ == '__main__':
    weighted_round_robin(
        rights=[1, 2, 4],
        valuations=[[11, 11, 22, 33, 44], [11, 22, 44, 55, 66], [11, 33, 22, 11, 66]],
        y=0.5)
    """
    TODO : add tests  
    """
