from settings import *

def loading_maps(map_name):
    with open(map_name,'r') as map_file:
        size = list(map(int,map_file.readline()[:-1].split('x')))
        structure = [i.split(',') for i in map_file.read().replace("\n","").split(';')]
        for i in range(size[1]):
            for j in range(size[0]):
                if structure[i][j] == 'i':
                    iron(j * 32, i * 32)
                if structure[i][j] == 'b':
                    brick(j * 32, i * 32)
                if structure[i][j] == 'p':
                    player(j * 32, i * 32)
                if structure[i][j] == 'p2':
                    player_2(j * 32, i * 32)
                if structure[i][j] == 'e':
                    tanks(j * 32, i * 32)