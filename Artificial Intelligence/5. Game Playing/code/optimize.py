import numpy as np


class HistoryTable:  # 历史启发算法
    def __init__(self):
        self.table = np.zeros((2, 90, 90))

    def GetHistoryScore(self, who,  step):
        return self.table[who, step.from_x * 9 + step.from_y, step.to_x * 9 + step.to_y]

    def AddHistoryScore(self, who,  step, depth):
        self.table[who, step.from_x * 9 + step.from_y, step.to_x * 9 + step.to_y] += 2 << depth


class Relation:
    def __init__(self):
        self.chess_type = 0
        self.num_attack = 0
        self.num_guard = 0
        self.num_attacked = 0
        self.num_guarded = 0
        self.attack = [0, 0, 0, 0, 0, 0]
        self.attacked = [0, 0, 0, 0, 0, 0]
        self.guard = [0, 0, 0, 0, 0, 0]
        self.guarded = [0, 0, 0, 0, 0, 0]

