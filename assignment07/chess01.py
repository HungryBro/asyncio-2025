import time
from datetime import timedelta

# Configuration
speed = 10000# คูณความเร็วเพื่อให้ไม่ต้องรอจริง
Judit_time = 5 / speed
Opponent_time = 55 / speed
opponents = 24
move_pairs = 30

def game(x):
    board_start_time = time.perf_counter()
    calculated_board_start_time = 0

    for i in range(move_pairs):
        # Judit move
        calculated_board_start_time += Judit_time
        print(f"BOARD-{x+1} {i+1} Judit made a move with {int(Judit_time*speed)} secs.")

        # Opponent move
        time.sleep(Opponent_time)  # รอจริง แต่ไวเพราะ speed สูง
        print(f"BOARD-{x+1} {i+1} Opponent made move with {int(Opponent_time*speed)} secs.")
        calculated_board_start_time += Opponent_time

    real_time = (time.perf_counter() - board_start_time) * speed
    print(f"BOARD-{x+1} - >>>>>>>>>>>>>>> Finished move in {real_time:.1f} secs")
    print(f"BOARD-{x+1} - >>>>>>>>>>>>>>> Finished move in {calculated_board_start_time*speed:.1f} secs (calculated)\n")

    return {
        'board_time': real_time,
        'calculated_board_time': calculated_board_start_time * speed
    }

if __name__ == "__main__":
    print(f"Number of games: {opponents} games.")
    print(f"Number of move: {move_pairs} pairs.")

    start_time = time.perf_counter()
    boards_time = 0
    calculated_board_time = 0

    for board in range(opponents):
        result = game(board)
        boards_time += result['board_time']
        calculated_board_time += result['calculated_board_time']

    print(f"Board exhibition finished for {opponents} opponents in {timedelta(seconds=round(boards_time))} hr.")
    print(f"Board exhibition finished for {opponents} opponents in {timedelta(seconds=round(calculated_board_time))} hr.  (calculated)")
    print(f"Finished in {round((time.perf_counter() - start_time)*speed)} secs.")
