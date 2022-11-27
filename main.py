#!/usr/bin/python3
import requests, sys
from sgfmill import sgf
players_info = ('PB', 'BR', 'PW', 'WR')

def get_sgf(sgfid:int):
    r = requests.get('https://getsgf.99weiqi.com/wxsgf.aspx?index={}'.format(sgfid))
    sgf_bin = r.content
    sgf_bin = sgf_bin[sgf_bin.find(b'('):]
    return sgf_bin.decode()


def modify_sgf(sgf_str):
    game = sgf.Sgf_game.from_string(sgf_str)
    if game.get_size() in [13, 19]:
        game.get_root().set('KM', '7.5')
    return game


def get_players(game):
    d = list()
    for i in players_info:
        d.append(game.get_root().get(i))
    return d

if __name__ == '__main__':
    assert sys.argv[1], "You didn't add any sgfid as argument."
    sgfid = int(sys.argv[1])
    sgf_str = get_sgf(sgfid)
    game = modify_sgf(sgf_str)
    players = get_players(game)
    filename = '{}「{}」 VS {}「{}」{}.sgf'.format(*players, sgfid)
    with open(filename, 'wb') as f:
        f.write(game.serialise())


