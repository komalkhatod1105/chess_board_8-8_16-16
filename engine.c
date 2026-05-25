#include <stdio.h>
#include <string.h>

#define SIZE8 8
#define SIZE16 16

char board[16][16][10];

int boardSize;
char currentPlayer;

// =========================
// INITIALIZE BOARD
// =========================

void initializeBoard(int size)
{
    boardSize = size;

    currentPlayer = 'W';

    // clear board

    for(int r=0;r<size;r++)
    {
        for(int c=0;c<size;c++)
        {
            strcpy(board[r][c], "");
        }
    }

    // =====================
    // 8x8
    // =====================

    if(size == 8)
    {
        char *top[] =
        {
            "r","n","b","q",
            "k","b","n","r"
        };

        char *bottom[] =
        {
            "R","N","B","Q",
            "K","B","N","R"
        };

        for(int i=0;i<8;i++)
        {
            strcpy(board[0][i], top[i]);

            strcpy(board[1][i], "p");

            strcpy(board[6][i], "P");

            strcpy(board[7][i], bottom[i]);
        }
    }

    // =====================
    // 16x16
    // =====================

    else
    {
        char *top16[] =
        {
            "r","n","b","q",
            "k","b","n","r",
            "r","n","b","q",
            "k","b","n","r"
        };

        char *bottom16[] =
        {
            "R","N","B","Q",
            "K","B","N","R",
            "R","N","B","Q",
            "K","B","N","R"
        };

        for(int i=0;i<16;i++)
        {
            strcpy(board[0][i], top16[i]);

            strcpy(board[1][i], "p");

            strcpy(board[14][i], "P");

            strcpy(board[15][i], bottom16[i]);
        }
    }
}

// =========================
// PRINT BOARD
// =========================

void printBoard()
{
    printf("\n");

    for(int r=0;r<boardSize;r++)
    {
        for(int c=0;c<boardSize;c++)
        {
            if(strcmp(board[r][c], "") == 0)
            {
                printf(". ");
            }
            else
            {
                printf("%s ", board[r][c]);
            }
        }

        printf("\n");
    }

    printf("\n");
}

// =========================
// VALIDATE MOVE
// =========================

int validMove(
    int fr,
    int fc,
    int tr,
    int tc
)
{
    // same position

    if(fr == tr && fc == tc)
    {
        return 0;
    }

    // board limits

    if(tr < 0 || tr >= boardSize)
    {
        return 0;
    }

    if(tc < 0 || tc >= boardSize)
    {
        return 0;
    }

    // empty source

    if(strcmp(board[fr][fc], "") == 0)
    {
        return 0;
    }

    return 1;
}

// =========================
// MOVE PIECE
// =========================

void movePiece(
    int fr,
    int fc,
    int tr,
    int tc
)
{
    strcpy(
        board[tr][tc],
        board[fr][fc]
    );

    strcpy(board[fr][fc], "");
}

// =========================
// SWITCH PLAYER
// =========================

void switchPlayer()
{
    if(currentPlayer == 'W')
    {
        currentPlayer = 'B';
    }
    else
    {
        currentPlayer = 'W';
    }
}

// =========================
// MAIN
// =========================

int main()
{
    int size;

    printf("Enter board size (8 or 16): ");

    scanf("%d",&size);

    initializeBoard(size);

    while(1)
    {
        int fr,fc,tr,tc;

        printBoard();

        printf(
            "Current Player: %c\n",
            currentPlayer
        );

        printf(
            "Enter move:\n"
        );

        printf(
            "fromRow fromCol toRow toCol\n"
        );

        scanf(
            "%d %d %d %d",
            &fr,
            &fc,
            &tr,
            &tc
        );

        if(validMove(
            fr,fc,tr,tc
        ))
        {
            movePiece(
                fr,fc,tr,tc
            );

            switchPlayer();
        }
        else
        {
            printf(
                "Invalid Move\n"
            );
        }
    }

    return 0;
}