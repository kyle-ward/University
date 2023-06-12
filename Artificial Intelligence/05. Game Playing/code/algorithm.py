import chess as cs
from constants import ChessConstants as cc
import optimize as op
import time


class Algorithm:
    def __init__(self):
        self.chessboard = cs.ChessBoard()
        self.max_depth = cc.max_depth
        self.history_table = op.HistoryTable()
        self.best_move = cs.Step()
        self.cnt = 0

    # alpha-beta剪枝，who == 0代表AI极大层，who == 1代表人类极小层
    # range(alpha, beta)
    def alpha_beta(self, depth, alpha, beta):
        who = (self.max_depth - depth) % 2
        # 判断是否游戏结束
        if self.game_over(who):
            return cc.min_val
        # 搜索到指定深度了，直接返回当前的评估值
        if depth == 1:
            return self.evaluate(who)
        # 返回当前棋局所有可能的走法
        move_list = self.chessboard.PossibleMove(who)

        # 获取每个走法对应的历史分数，初始化为全0
        for i in range(len(move_list)):
            move_list[i].score = self.history_table.GetHistoryScore(who, move_list[i])
            pass
        # 历史分数最小的将被优先遍历
        # 总遍历深度：将每次遍历的深度累加
        # 故最优先遍历的是那些从未到达过的棋局，然后依次按照总遍历深度的次序遍历
        move_list.sort()
        best_step = move_list[0]
        for step in move_list:
            temp = self.move_to(step)
            # 通过去负号来避免分类讨论，等于每一层都是最大层（相对who而言）
            score = -self.alpha_beta(depth - 1, -beta, -alpha)
            self.move_back(step, temp)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
                # 记录生成博弈树第一层的对应最佳走法作为AI下一步的走法
                if depth == self.max_depth:
                    self.best_move = step
                # 此时的得分已经超过了alpha，故更新alpha，同时当前走法是目前的最优解
                best_step = step
            '''
            if score > alpha:
                alpha = score
                # 记录生成博弈树第一层的对应最佳走法作为AI下一步的走法
                if depth == self.max_depth:
                    self.best_move = step
                best_step = step
            if alpha >= beta:
                best_step = step
                return beta
            '''
        # 更新历史表，如果best_step非空
        if best_step.from_x != -1:
            # 历史分数加上当前的深度值
            self.history_table.AddHistoryScore(who, best_step, depth)
            pass
        return alpha

    # who表示该谁走，返回评分值
    def evaluate(self, who):
        self.cnt += 1
        relation_list = self.relation_list_init()
        base_val = [0, 0]
        pos_val = [0, 0]
        mobile_val = [0, 0]
        relation_val = [0, 0]
        for x in range(9):
            for y in range(10):
                now_chess = self.chessboard.board[x][y]
                _type = now_chess.chess_type
                if _type == 0:
                    continue
                # now = 0 if who else 1
                now = now_chess.belong
                pos = x * 9 + y
                temp_move_list = self.chessboard.GetChessMove(x, y, now, True)
                # 计算基础价值
                base_val[now] += cc.base_val[_type]
                # 计算位置价值
                if now == 0:
                    # 如果是要求最大值的玩家
                    pos_val[now] += cc.pos_val[_type][pos]
                else:
                    pos_val[now] += cc.pos_val[_type][89 - pos]
                # 计算机动性价值，记录关系信息
                for item in temp_move_list:
                    # 目的位置的棋子
                    temp_chess = self.chessboard.board[item.to_x][item.to_y]
                    if temp_chess.chess_type == cc.nul:
                        # 如果是空，那么加上机动性值
                        mobile_val[now] += cc.mobile_val[_type]
                        continue
                    elif temp_chess.belong != now:
                        # 如果不是自己一方的棋子
                        if temp_chess.chess_type == cc.kng:
                            # 如果能吃了对方的将，那么就赢了
                            if temp_chess.belong != who:
                                return cc.max_val
                            else:
                                relation_val[1 - now] -= 20
                                # 如果不能，那么就相当于被将军，对方要减分
                                continue
                        # 记录now_chess攻击了谁
                        relation_list[x][y].attack[relation_list[x][y].num_attack] = temp_chess.chess_type
                        relation_list[x][y].num_attack += 1
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type
                        # 记录temp_chess被谁攻击
                        relation_list[item.to_x][item.to_y].attacked[
                            relation_list[item.to_x][item.to_y].num_attacked] = _type
                        relation_list[item.to_x][item.to_y].num_attacked += 1
                    elif temp_chess.belong == now:
                        if temp_chess.chess_type == cc.kng:  # 保护自己的将没有意义，直接跳过
                            continue
                        # 记录now_chess保护了谁
                        relation_list[x][y].guard[relation_list[x][y].num_guard] = temp_chess
                        relation_list[x][y].num_guard += 1
                        # 记录temp_chess被谁所保护
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type
                        relation_list[item.to_x][item.to_y].guarded[
                            relation_list[item.to_x][item.to_y].num_guarded] = _type
                        relation_list[item.to_x][item.to_y].num_guarded += 1
        for x in range(9):
            for y in range(10):
                num_attacked = relation_list[x][y].num_attacked
                num_guarded = relation_list[x][y].num_guarded
                now_chess = self.chessboard.board[x][y]
                _type = now_chess.chess_type
                now = now_chess.belong
                unit_val = cc.base_val[now_chess.chess_type] >> 3
                sum_attack = 0  # 被攻击总子力
                sum_guard = 0
                min_attack = 999  # 最小的攻击者
                max_attack = 0  # 最大的攻击者
                max_guard = 0
                flag = 999  # 有没有比这个子的子力小的
                if _type == cc.nul:
                    continue
                # 统计攻击方的子力
                for i in range(num_attacked):
                    temp = cc.base_val[relation_list[x][y].attacked[i]]
                    flag = min(flag, min(temp, cc.base_val[_type]))
                    min_attack = min(min_attack, temp)
                    max_attack = max(max_attack, temp)
                    sum_attack += temp
                # 统计防守方的子力
                for i in range(num_guarded):
                    temp = cc.base_val[relation_list[x][y].guarded[i]]
                    max_guard = max(max_guard, temp)
                    sum_guard += temp
                if num_attacked == 0:
                    relation_val[now] += 5 * relation_list[x][y].num_guarded
                else:
                    multi_val = 5 if who != now else 1
                    if num_guarded == 0:
                        # 如果没有保护
                        relation_val[now] -= multi_val * unit_val
                    else:
                        # 如果有保护
                        if flag != 999:
                            # 存在攻击者子力小于被攻击者子力,对方将愿意换子
                            relation_val[now] -= multi_val * unit_val
                            relation_val[1 - now] -= multi_val * (flag >> 3)
                        # 如果是二换一, 并且最小子力小于被攻击者子力与保护者子力之和, 则对方可能以一子换两子
                        elif num_guarded == 1 and num_attacked > 1 and \
                                min_attack < cc.base_val[_type] + sum_guard:
                            relation_val[now] -= multi_val * unit_val
                            relation_val[now] -= multi_val * (sum_guard >> 3)
                            relation_val[1 - now] -= multi_val * (flag >> 3)
                        # 如果是三换二并且攻击者子力较小的二者之和小于被攻击者子力与保护者子力之和,则对方可能以两子换三子
                        elif num_guarded == 2 and num_attacked == 3 and \
                                sum_attack - max_attack < cc.base_val[_type] + sum_guard:
                            relation_val[now] -= multi_val * unit_val
                            relation_val[now] -= multi_val * (sum_guard >> 3)
                            relation_val[1 - now] -= multi_val * ((sum_attack - max_attack) >> 3)
                        # 如果是n换n，攻击方与保护方数量相同并且攻击者子力小于被攻击者子力与保护者子力之和再减去保护者中最大子力,则对方可能以n子换n子
                        elif num_guarded == num_attacked and \
                                sum_attack < cc.base_val[now_chess.chess_type] + sum_guard - max_guard:
                            relation_val[now] -= multi_val * unit_val
                            relation_val[now] -= multi_val * ((sum_guard - max_guard) >> 3)
                            relation_val[1 - now] -= sum_attack >> 3
        my_max_val = base_val[0] + pos_val[0] + mobile_val[0] + relation_val[0]
        my_min_val = base_val[1] + pos_val[1] + mobile_val[1] + relation_val[1]
        if who == 0:
            return my_max_val - my_min_val
        else:
            return my_min_val - my_max_val

    # 初始化棋盘的关系类矩阵
    @staticmethod
    def relation_list_init():
        res_list = []
        for i in range(9):
            res_list.append([])
            for j in range(10):
                res_list[i].append(op.Relation())
        return res_list

    # 判断游戏是否结束
    def game_over(self, who):
        for i in range(9):
            for j in range(10):
                if self.chessboard.board[i][j].chess_type == cc.kng:
                    if self.chessboard.board[i][j].belong == who:
                        return False
        return True

    # 移动棋子
    def move_to(self, step):
        belong = self.chessboard.board[step.to_x][step.to_y].belong
        chess_type = self.chessboard.board[step.to_x][step.to_y].chess_type
        temp = cs.ChessProperty(belong, chess_type)
        self.chessboard.board[step.to_x][step.to_y].chess_type = \
            self.chessboard.board[step.from_x][step.from_y].chess_type
        self.chessboard.board[step.to_x][step.to_y].belong = \
            self.chessboard.board[step.from_x][step.from_y].belong
        self.chessboard.board[step.from_x][step.from_y].chess_type = cc.nul
        self.chessboard.board[step.from_x][step.from_y].belong = -1
        return temp

    # 恢复棋子
    def move_back(self, step, chess):
        self.chessboard.board[step.from_x][step.from_y].belong = \
            self.chessboard.board[step.to_x][step.to_y].belong
        self.chessboard.board[step.from_x][step.from_y].chess_type = \
            self.chessboard.board[step.to_x][step.to_y].chess_type
        self.chessboard.board[step.to_x][step.to_y].belong = chess.belong
        self.chessboard.board[step.to_x][step.to_y].chess_type = chess.chess_type


def Process(pieces_list, x1, y1, x2, y2, algorithm_init):
    s = cs.Step(8 - x1, y1, 8 - x2, y2)

    print('human\'s', s)
    algorithm_init.move_to(s)

    start = time.perf_counter()
    algorithm_init.alpha_beta(cc.max_depth, cc.min_val, cc.max_val)
    end = time.perf_counter()
    t = algorithm_init.best_move
    algorithm_init.move_to(t)

    print('AI\'s', t)
    print('Evaluate times:', algorithm_init.cnt)
    print('Process time:', end - start)

    list_move_enable = []
    for i in range(0, 9):
        for j in range(0, 10):
            for item in pieces_list:
                if item.x == 8 - t.from_x and item.y == t.from_y:
                    list_move_enable.append([item, 8 - t.to_x, t.to_y])
    pieces_best = list_move_enable[0]
    print('-----------------------------------------------------------------')
    return [pieces_best[0].x, pieces_best[0].y, pieces_best[1], pieces_best[2]]
