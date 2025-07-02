# example of waiting for all tasks to complete
from random import random
import asyncio

# coroutine to execute in new task
async def task_coro(arg):
    # generate a random value between 0 and 1
    value = random()
    # block for a moment
    await asyncio.sleep(value)
    # report the value
    print(f'>task {arg} done with {value}')

# main courutine
async def main():
    # create many tassks
    tasks = [asyncio.create_task(task_coro(i)) for i in range (10)]
    # wait for all tasks to complete
    # done,pending = await asyncio.wait(tasks,return_when = asyncio.ALL_COMPLETED)
    done,pending = await asyncio.wait(tasks)
    # report results
    print('All odne')

# start the sysncio program
asyncio.run(main())
