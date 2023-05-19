import pygame
import pieces
from constants import GeneralConstants as gc
from algorithm import *


class ChineseChess:
    window = None
    Start_X = gc.Start_X
    Start_Y = gc.Start_Y
    Interval = gc.Interval
    Max_X = Start_X + 8 * Interval
    Max_Y = Start_Y + 9 * Interval
    from_x = 0
    from_y = 0
    to_x = 0
    to_y = 0
    x_before_click = -1
    y_before_click = -1

    algorithm_init = Algorithm()
    player1Color = gc.player1Color
    player2Color = gc.player2Color
    # 记录回合状态
    PutDownFlag = player1Color
    piecesSelected = None

    piecesList = []

    # 游戏开始
    def start_game(self):
        self.window = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT])
        pygame.display.set_caption("中国象棋")
        self.piecesInit()

        # 游戏界面循环
        while True:
            time.sleep(0.1)
            # 获取事件
            self.window.fill(gc.BG_COLOR)
            # 绘制棋盘棋子
            self.drawChessboard()
            self.PiecesDisplay()
            # 判断是否存在输赢
            self.VictoryOrDefeat()
            # 电脑下棋（如果是它的回合）
            self.ComputerPlay()
            # 获取鼠标事件
            self.getEvent()
            # 刷新游戏界面
            pygame.display.update()
            pygame.display.flip()

    def drawChessboard(self):
        background_color = pygame.image.load("images/bg.jpg")
        background_image = pygame.image.load("images/bg.png")
        self.window.blit(background_color, (0, 0))
        self.window.blit(background_color, (0, 270))
        self.window.blit(background_color, (0, 540))
        self.window.blit(background_image, (70, 40))

    def piecesInit(self):
        self.piecesList.append(pieces.Rooks(self.player2Color, 0, 0))
        self.piecesList.append(pieces.Rooks(self.player2Color,  8, 0))
        self.piecesList.append(pieces.Elephants(self.player2Color,  2, 0))
        self.piecesList.append(pieces.Elephants(self.player2Color,  6, 0))
        self.piecesList.append(pieces.King(self.player2Color, 4, 0))
        self.piecesList.append(pieces.Knight(self.player2Color,  1, 0))
        self.piecesList.append(pieces.Knight(self.player2Color,  7, 0))
        self.piecesList.append(pieces.Cannons(self.player2Color,  1, 2))
        self.piecesList.append(pieces.Cannons(self.player2Color, 7, 2))
        self.piecesList.append(pieces.Mandarins(self.player2Color,  3, 0))
        self.piecesList.append(pieces.Mandarins(self.player2Color, 5, 0))
        self.piecesList.append(pieces.Pawns(self.player2Color, 0, 3))
        self.piecesList.append(pieces.Pawns(self.player2Color, 2, 3))
        self.piecesList.append(pieces.Pawns(self.player2Color, 4, 3))
        self.piecesList.append(pieces.Pawns(self.player2Color, 6, 3))
        self.piecesList.append(pieces.Pawns(self.player2Color, 8, 3))

        self.piecesList.append(pieces.Rooks(self.player1Color,  0, 9))
        self.piecesList.append(pieces.Rooks(self.player1Color,  8, 9))
        self.piecesList.append(pieces.Elephants(self.player1Color, 2, 9))
        self.piecesList.append(pieces.Elephants(self.player1Color, 6, 9))
        self.piecesList.append(pieces.King(self.player1Color,  4, 9))
        self.piecesList.append(pieces.Knight(self.player1Color, 1, 9))
        self.piecesList.append(pieces.Knight(self.player1Color, 7, 9))
        self.piecesList.append(pieces.Cannons(self.player1Color,  1, 7))
        self.piecesList.append(pieces.Cannons(self.player1Color,  7, 7))
        self.piecesList.append(pieces.Mandarins(self.player1Color,  3, 9))
        self.piecesList.append(pieces.Mandarins(self.player1Color,  5, 9))
        self.piecesList.append(pieces.Pawns(self.player1Color, 0, 6))
        self.piecesList.append(pieces.Pawns(self.player1Color, 2, 6))
        self.piecesList.append(pieces.Pawns(self.player1Color, 4, 6))
        self.piecesList.append(pieces.Pawns(self.player1Color, 6, 6))
        self.piecesList.append(pieces.Pawns(self.player1Color, 8, 6))

    # 打印棋子
    def PiecesDisplay(self):
        for item in self.piecesList:
            item.DisplayPieces(self.window)

    def getEvent(self):
        # 获取所有的事件
        event_list = pygame.event.get()
        for event in event_list:
            # 如果点击到X键
            if event.type == pygame.QUIT:
                self.endGame()
            # 检测到鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标位置
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                # 判断是否在棋盘内，不然输出out
                if (self.Start_X - self.Interval / 2 < mouse_x < self.Max_X + self.Interval / 2) and \
                        (self.Start_Y - self.Interval / 2 < mouse_y < self.Max_Y + self.Interval / 2):
                    # 不是自己回合时点击无效
                    if self.PutDownFlag != self.player1Color:
                        return

                    click_x = round((mouse_x - self.Start_X) / self.Interval)
                    click_y = round((mouse_y - self.Start_Y) / self.Interval)
                    click_mod_x = (mouse_x - self.Start_X) % self.Interval
                    click_mod_y = (mouse_y - self.Start_Y) % self.Interval
                    # 判断是否是有效点击
                    if abs(click_mod_x - self.Interval / 2) >= 5 and abs(
                            click_mod_y - self.Interval / 2) >= 5:
                        # 有效点击点
                        self.from_x = self.x_before_click
                        self.from_y = self.y_before_click
                        self.to_x = click_x
                        self.to_y = click_y
                        print('有效点击：(' + str(click_x) + ', ' + str(click_y) + ')')
                        self.x_before_click = click_x
                        self.y_before_click = click_y
                        # 在对应点放置棋子
                        self.PutDownPieces(click_x, click_y)
                    else:
                        print('无效点击')
                else:
                    print("out")

    def PutDownPieces(self, x, y):
        select_filter = list(filter(lambda cm: cm.x == x and cm.y == y and cm.player == self.player1Color, self.piecesList))
        if len(select_filter):
            self.piecesSelected = select_filter[0]
            return

        # 如果有棋子符合要求
        if self.piecesSelected:
            arr = pieces.listPiecesToArr(self.piecesList)
            # 如果要求移动到的位置合法
            if self.piecesSelected.can_move(arr, x, y):
                self.PiecesMove(self.piecesSelected, x, y)
                # 转换下棋角色
                self.PutDownFlag = self.player2Color
        else:
            fi = filter(lambda p: p.x == x and p.y == y, self.piecesList)
            list_fi = list(fi)
            if len(list_fi) != 0:
                self.piecesSelected = list_fi[0]

    # 棋子移动函数
    def PiecesMove(self, pieces, x, y):
        for item in self.piecesList:
            if item.x == x and item.y == y:
                self.piecesList.remove(item)
        pieces.x = x
        pieces.y = y
        # print("move to " + str(x) + " " + str(y))
        return True

    # 电脑下棋函数
    def ComputerPlay(self):
        if self.PutDownFlag == self.player2Color:
            print("轮到电脑了")
            best_move = Process(self.piecesList, self.from_x, self.from_y, self.to_x, self.to_y, self.algorithm_init)
            piece_move = None
            for item in self.piecesList:
                if item.x == best_move[0] and item.y == best_move[1]:
                    piece_move = item

            # 按照best_move落子并转换角色
            self.PiecesMove(piece_move, best_move[2], best_move[3])
            self.PutDownFlag = self.player1Color

    # 判断游戏胜利
    def VictoryOrDefeat(self):
        txt = ""
        result = [self.player1Color, self.player2Color]
        for item in self.piecesList:
            if type(item) == pieces.King:
                if item.player == self.player1Color:
                    result.remove(self.player1Color)
                if item.player == self.player2Color:
                    result.remove(self.player2Color)

        if len(result) == 0:
            return
        if result[0] == self.player1Color:
            txt = "失败！"
        else:
            txt = "胜利！"
        self.window.blit(self.getTextSurface("%s" % txt), (gc.SCREEN_WIDTH - 100, 200))
        self.PutDownFlag = gc.overColor

    @staticmethod
    def getTextSurface(text):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 18)
        txt = font.render(text, True, gc.TEXT_COLOR)
        return txt

    @staticmethod
    def endGame():
        print("exit")
        exit()


if __name__ == '__main__':
    start_game = ChineseChess()
    start_game.start_game()
