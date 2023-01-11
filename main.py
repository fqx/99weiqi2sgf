#!/usr/bin/python3
import requests, sys, re
from sgfmill import sgf
players_info = ('PB', 'BR', 'PW', 'WR')
id_re = re.compile('sgfid=(\d+)')


def error_func(error_code):
    error_codes = {
        100: "输入错误，按任意键退出。"
    }
    input(error_codes[error_code])
    exit(error_code)


def get_sgfid(url):
    try:
        sgfid = int(id_re.search(url).groups()[0])
    except (IndexError, AttributeError):
        error_func(100)
    return sgfid


def get_sgf(sgfid:int):
    r = requests.get('https://getsgf.99weiqi.com/wxsgf.aspx?index={}'.format(sgfid), timeout=5)
    sgf_bin = r.content
    sgf_bin = sgf_bin[sgf_bin.find(b'(;'):]
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
    # assert sys.argv[1], "You didn't add any sgfid as argument."
    try:
        sgfid = int(sys.argv[1])
    except ValueError:
        sgfid = get_sgfid(sys.argv[1])
    except IndexError:
        link = input('请输入99围棋分享链接或sgfid：')
        try:
            sgfid = int(link)
        except ValueError:
            sgfid = get_sgfid(link)
        except:
            error_func(100)
    sgf_str = get_sgf(sgfid)
    game = modify_sgf(sgf_str)
    players = get_players(game)
    filename = '{}「{}」 VS {}「{}」{}.sgf'.format(*players, sgfid)
    with open(filename, 'wb') as f:
        f.write(game.serialise())


