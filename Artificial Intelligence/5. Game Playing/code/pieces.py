from constants import GeneralConstants as gc


class Pieces:
    def __init__(self, player,  x, y, name=''):
        self.x = x
        self.y = y
        self.name = name
        self.player = player
        self.image_key = self.getImageKey()
        self.image = gc.pieces_images[self.image_key]
        self.rect = self.image.get_rect()
        self.rect.left = gc.Start_X + x * gc.Interval - self.image.get_rect().width / 2
        self.rect.top = gc.Start_Y + y * gc.Interval - self.image.get_rect().height / 2

    def __str__(self):
        return self.getImageKey() + '\t\t(' + str(self.x) + ', ' + str(self.y) + ')'

    def getImageKey(self):
        return ('r' if self.player == 1 else 'b') + '_' + self.name

    def DisplayPieces(self, screen):
        self.rect.left = gc.Start_X + self.x * gc.Interval - self.image.get_rect().width / 2
        self.rect.top = gc.Start_Y + self.y * gc.Interval - self.image.get_rect().height / 2
        screen.blit(self.image, self.rect)

    def can_move(self, arr, moveto_x, moveto_y):
        return None


class Rooks(Pieces):
    def __init__(self, player,  x, y):
        self.player = player
        super().__init__(player,  x, y)

    def getImageKey(self):
        if self.player == gc.player1Color:
            return "r_rook"
        else:
            return "b_rook"

    def can_move(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if self.x == moveto_x:
            step = -1 if self.y > moveto_y else 1
            for i in range(self.y + step, moveto_y, step):
                if arr[self.x][i] != 0:
                    return False
            return True

        if self.y == moveto_y:
            step = -1 if self.x > moveto_x else 1
            for i in range(self.x + step, moveto_x, step):
                if arr[i][self.y] != 0:
                    return False
            return True


class Knight(Pieces):
    def __init__(self, player,  x, y):
        self.player = player
        super().__init__(player,  x, y)
    
    def getImageKey(self):
        if self.player == gc.player1Color:
            return "r_knight"
        else:
            return "b_knight"
    
    def can_move(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False

        move_x = moveto_x-self.x
        move_y = moveto_y - self.y
        if abs(move_x) == 1 and abs(move_y) == 2:
            step = 1 if move_y > 0 else -1
            if arr[self.x][self.y + step] == 0:
                return True
        if abs(move_x) == 2 and abs(move_y) == 1:
            step = 1 if move_x > 0 else -1
            if arr[self.x + step][self.y] == 0:
                return True


class Elephants(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImageKey(self):
        if self.player == gc.player1Color:
            return "r_elephant"
        else:
            return "b_elephant"

    def can_move(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if self.y <= 4 and moveto_y >= 5 or self.y >= 5 and moveto_y <= 4:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y
        if abs(move_x) == 2 and abs(move_y) == 2:
            step_x = 1 if move_x > 0 else -1
            step_y = 1 if move_y > 0 else -1
            if arr[self.x + step_x][self.y + step_y] == 0:
                return True


class Mandarins(Pieces):
    def __init__(self, player,  x, y):
        self.player = player
        super().__init__(player,  x, y)

    def getImageKey(self):
        if self.player == gc.player1Color:
            return "r_mandarin"
        else:
            return "b_mandarin"

    def can_move(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if moveto_x < 3 or moveto_x > 5:
            return False
        if 2 < moveto_y < 7:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y
        if abs(move_x) == 1 and abs(move_y) == 1:
            return True


class King(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImageKey(self):
        if self.player == gc.player1Color:
            return "r_king"
        else:
            return "b_king"

    def can_move(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        if moveto_x < 3 or moveto_x > 5:
            return False
        if 2 < moveto_y < 7:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y
        if abs(move_x) + abs(move_y) == 1:
            return True


class Cannons(Pieces):
    def __init__(self, player,  x, y):
        self.player = player
        super().__init__(player, x, y)

    def getImageKey(self):
        if self.player == gc.player1Color:
            return "r_cannon"
        else:
            return "b_cannon"

    def can_move(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        over_flag = False
        if self.x == moveto_x:
            step = -1 if self.y > moveto_y else 1
            for i in range(self.y + step, moveto_y, step):
                if arr[self.x][i] != 0:
                    if over_flag:
                        return False
                    else:
                        over_flag = True

            if over_flag and arr[moveto_x][moveto_y] == 0:
                return False
            if not over_flag and arr[self.x][moveto_y] != 0:
                return False

            return True

        if self.y == moveto_y:
            step = -1 if self.x > moveto_x else 1
            for i in range(self.x + step, moveto_x, step):
                if arr[i][self.y] != 0:
                    if over_flag:
                        return False
                    else:
                        over_flag = True

            if over_flag and arr[moveto_x][moveto_y] == 0:
                return False
            if not over_flag and arr[moveto_x][self.y] != 0:
                return False
            return True


class Pawns(Pieces):
    def __init__(self, player, x, y):
        self.player = player
        super().__init__(player,  x, y)

    def getImageKey(self):
        if self.player == gc.player1Color:
            return "r_pawn"
        else:
            return "b_pawn"

    def can_move(self, arr, moveto_x, moveto_y):
        if self.x == moveto_x and self.y == moveto_y:
            return False
        if arr[moveto_x][moveto_y] == self.player:
            return False
        move_x = moveto_x - self.x
        move_y = moveto_y - self.y

        if self.player == gc.player1Color:
            if self.y > 4 and move_x != 0:
                return False
            if move_y > 0:
                return False
        elif self.player == gc.player2Color:
            if self.y <= 4 and move_x != 0:
                return False
            if move_y < 0:
                return False

        if abs(move_x) + abs(move_y) == 1:
            return True


def listPiecesToArr(pieces_list):
    arr = [[0 for i in range(10)] for j in range(9)]
    for i in range(0, 9):
        for j in range(0, 10):
            if len(list(filter(lambda cm: cm.x == i and cm.y == j and cm.player == gc.player1Color,
                               pieces_list))):
                arr[i][j] = gc.player1Color
            elif len(list(filter(lambda cm: cm.x == i and cm.y == j and cm.player == gc.player2Color,
                                 pieces_list))):
                arr[i][j] = gc.player2Color
    return arr
