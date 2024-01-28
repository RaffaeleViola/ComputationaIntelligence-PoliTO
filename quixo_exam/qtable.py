from game import Move, Game
from tqdm import tqdm


def read_tuple(tup: str):
    tmp = tup.replace('(', "")
    tmp = tmp.replace(')', "")
    nums = tmp.split(',')
    return tuple([int(num.strip()) for num in nums])


def read_action(tup: str):
    map_enum = {0: Move.TOP,
                1: Move.BOTTOM,
                2: Move.LEFT,
                3: Move.RIGHT}
    tmp = tup.replace('(', "")
    tmp = tmp.replace(')', "")
    unpacked = tmp.split(',')
    num1, num2, move = int(unpacked[0]), int(unpacked[1]), int(unpacked[2].strip())
    e1 = (num1, num2)
    e2 = map_enum[move]
    return e1, e2


class Qtable:
    def __init__(self):
        self.table = dict()  # state:{actions: value) value dfault is 0 -> action is ((0,0),3)

    def store(self, path):
        map_enum = {Move.TOP: 0,
                    Move.BOTTOM: 1,
                    Move.LEFT: 2,
                    Move.RIGHT: 3}
        with open(path, "w") as f:
            for state, actions in self.table.items():
                to_list = [str(state)]
                for act, val in actions.items():
                    strip_act = f"({str(act[0])},{str(map_enum[act[1]])})"
                    to_list.append(f"{strip_act}={val}")
                to_write = ';'.join(to_list)
                f.write(f'{to_write}\n')

    def load(self, path):
        with open(path, "r") as f:
            print('Loading Table...')
            for line in tqdm(f.readlines()):
                words = line.strip().split(";")
                key = read_tuple(words[0])
                tmp_dict = dict()
                for word in words[1:]:
                    act_val = word.split("=")
                    act = read_action(act_val[0])
                    val = float(act_val[1])
                    tmp_dict[act] = val
                self.table[key] = tmp_dict
            print('Table Loaded')

    def get_table(self):
        return self.table

    def __contains__(self, item):
        return item in self.table

    def __getitem__(self, item):
        return self.table[item]

    def __setitem__(self, key, value):
        self.table[key] = value

