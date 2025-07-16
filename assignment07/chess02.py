import time
import asyncio
from datetime import timedelta

# --- CONFIG ---
speed = 100
JUDIT_TIME = 5 / speed
OPPONENT_TIME = 55 / speed
move_pairs = 30
opponents = 24

async def play_game(board_id):
    board_start = time.perf_counter()
    calculated_time = 0

    for i in range(1, move_pairs + 1):
        # Judit move
        time.sleep(JUDIT_TIME)
        calculated_time += JUDIT_TIME
        print(f"BOARD-{board_id} {i} Judit made a move with {int(JUDIT_TIME * speed)} secs.")

        # Opponent move (non-blocking)
        await asyncio.sleep(OPPONENT_TIME)
        calculated_time += OPPONENT_TIME
        print(f"BOARD-{board_id} {i} Opponent made move with {int(OPPONENT_TIME * speed)} secs.")

    real_time = (time.perf_counter() - board_start) * speed
    return board_id, real_time, calculated_time * speed

async def main():
    print(f"Number of games: {opponents} games.")
    print(f"Number of move: {move_pairs} pairs.\n")

    start_time = time.perf_counter()

    # Start all board games concurrently
    tasks = [asyncio.create_task(play_game(i + 1)) for i in range(opponents)]
    results = await asyncio.gather(*tasks)  # List of tuples: (board_id, real_time, calculated_time)

    # Sort results by board_id to keep output ordered
    results.sort(key=lambda x: x[0])

    for board_id, real_time, calculated_time in results:
        print(f"BOARD-{board_id} – 30 Opponent made move with {int(OPPONENT_TIME * speed)} secs.")
        print(f"BOARD-{board_id} – >>>>>>>>>>>>>>> Finished move in {real_time:.1f} secs\n")

    total_real_time = max(r[1] for r in results)
    total_time_formatted = timedelta(seconds=round(total_real_time))
    print(f"Board exhibition finished for {opponents} opponents in {total_time_formatted} hr.")

asyncio.run(main())
