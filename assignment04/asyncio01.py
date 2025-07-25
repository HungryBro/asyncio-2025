# example of getting the current task from the main coroutine
import asyncio

# define a main coroutine
async def main():
    # report a meesage
    print('main coroutine started')
    # get the current task
    task = asyncio.current_task()
    # report its details
    print(task)

# start the asyncio program
asyncio.run(main())
