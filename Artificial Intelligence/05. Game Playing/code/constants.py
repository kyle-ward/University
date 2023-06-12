import pygame


class GeneralConstants:
    SCREEN_WIDTH = 650
    SCREEN_HEIGHT = 650
    Start_X = 85
    Start_Y = 50
    Interval = 59

    player1Color = 1
    player2Color = 2
    overColor = 3

    BG_COLOR = pygame.Color(200, 200, 200)
    Line_COLOR = pygame.Color(255, 255, 200)
    TEXT_COLOR = pygame.Color(255, 0, 0)

    # 定义颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    repeat = 0

    pieces_images = {
        'b_rook': pygame.image.load("images/b_c.gif"),
        'b_elephant': pygame.image.load("images/b_x.gif"),
        'b_king': pygame.image.load("images/b_j.gif"),
        'b_knight': pygame.image.load("images/b_m.gif"),
        'b_mandarin': pygame.image.load("images/b_s.gif"),
        'b_cannon': pygame.image.load("images/b_p.gif"),
        'b_pawn': pygame.image.load("images/b_z.gif"),

        'r_rook': pygame.image.load("images/r_c.gif"),
        'r_elephant': pygame.image.load("images/r_x.gif"),
        'r_king': pygame.image.load("images/r_j.gif"),
        'r_knight': pygame.image.load("images/r_m.gif"),
        'r_mandarin': pygame.image.load("images/r_s.gif"),
        'r_cannon': pygame.image.load("images/r_p.gif"),
        'r_pawn': pygame.image.load("images/r_z.gif"),
    }

    pos_list = [[0, 0], [8, 0], [2, 0], [6, 0], [4, 0], [1, 0], [7, 0], [1, 2],
                [7, 2], [3, 0], [5, 0], [0, 3], [2, 3], [4, 3], [6, 3], [8, 3]]
    name_list = ['rook', 'rook', 'elephant', 'elephant', 'king', 'knight', 'knight',
                 'cannon', 'cannon', 'mandarin', 'mandarin', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']


class ChessConstants:
    # 两个玩家
    my_max = True
    my_min = False
    # 八个棋子
    nul = 0
    kng = 1
    rok = 2
    mrd = 3
    cnn = 4
    elt = 5
    knt = 6
    pwn = 7
    # 初始化的棋盘
    initial_chessboard = [
        [rok, nul, nul, pwn, nul, nul, pwn, nul, nul, rok],
        [mrd, nul, cnn, nul, nul, nul, nul, cnn, nul, mrd],
        [elt, nul, nul, pwn, nul, nul, pwn, nul, nul, elt],
        [knt, nul, nul, nul, nul, nul, nul, nul, nul, knt],
        [kng, nul, nul, pwn, nul, nul, pwn, nul, nul, kng],
        [knt, nul, nul, nul, nul, nul, nul, nul, nul, knt],
        [elt, nul, nul, pwn, nul, nul, pwn, nul, nul, elt],
        [mrd, nul, cnn, nul, nul, nul, nul, cnn, nul, mrd],
        [rok, nul, nul, pwn, nul, nul, pwn, nul, nul, rok]
    ]
    # 最大步数
    max_depth = 4
    # 最大值，最小值
    max_val = float("inf")
    min_val = float("-inf")
    # 评估方法
    base_val = [0, 0, 500, 300, 300, 250, 250, 80]
    mobile_val = [0, 0, 6, 12, 6, 1, 1, 15]
    pos_val = [
        [  # 空
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [  # 将
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
            5, -8, -9, 0, 0, 0, 0, 0, 0, 0,
            1, -8, -9, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ],
        [  # 车
            -6, 5, -2, 4, 8, 8, 6, 6, 6, 6,
            6, 8, 8, 9, 12, 11, 13, 8, 12, 8,
            4, 6, 4, 4, 12, 11, 13, 7, 9, 7,
            12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
            0, 0, 12, 14, 15, 15, 16, 16, 33, 14,
            12, 12, 12, 12, 14, 14, 16, 14, 16, 13,
            4, 6, 4, 4, 12, 11, 13, 7, 9, 7,
            6, 8, 8, 9, 12, 11, 13, 8, 12, 8,
            -6, 5, -2, 4, 8, 8, 6, 6, 6, 6
        ],
        [  # 马
            0, -3, 5, 4, 2, 2, 5, 4, 2, 2,
            -3, 2, 4, 6, 10, 12, 20, 10, 8, 2,
            2, 4, 6, 10, 13, 11, 12, 11, 15, 2,
            0, 5, 7, 7, 14, 15, 19, 15, 9, 8,
            2, -10, 4, 10, 15, 16, 12, 11, 6, 2,
            0, 5, 7, 7, 14, 15, 19, 15, 9, 8,
            2, 4, 6, 10, 13, 11, 12, 11, 15, 2,
            -3, 2, 4, 6, 10, 12, 20, 10, 8, 2,
            0, -3, 5, 4, 2, 2, 5, 4, 2, 2
        ],
        [  # 炮
            0, 0, 1, 0, -1, 0, 0, 1, 2, 4,
            0, 1, 0, 0, 0, 0, 3, 1, 2, 4,
            1, 2, 4, 0, 3, 0, 3, 0, 0, 0,
            3, 2, 3, 0, 0, 0, 2, -5, -4, -5,
            3, 2, 5, 0, 4, 4, 4, -4, -7, -6,
            3, 2, 3, 0, 0, 0, 2, -5, -4, -5,
            1, 2, 4, 0, 3, 0, 3, 0, 0, 0,
            0, 1, 0, 0, 0, 0, 3, 1, 2, 4,
            0, 0, 1, 0, -1, 0, 0, 1, 2, 4
        ],
        [  # 相
            0, 0, -2, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, -2, 0, 0, 0, 0, 0, 0, 0
        ],
        [  # 士
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ],
        [  # 兵
            0, 0, 0, -2, 3, 10, 20, 20, 20, 0,
            0, 0, 0, 0, 0, 18, 27, 30, 30, 0,
            0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
            0, 0, 0, 0, 0, 35, 40, 55, 65, 2,
            0, 0, 0, 6, 7, 40, 42, 55, 70, 4,
            0, 0, 0, 0, 0, 35, 40, 55, 65, 2,
            0, 0, 0, -2, 4, 22, 30, 45, 50, 0,
            0, 0, 0, 0, 0, 18, 27, 30, 30, 0,
            0, 0, 0, -2, 3, 10, 20, 20, 20, 0
        ]
    ]
