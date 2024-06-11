import asyncio
from  loguru  import logger

async def func1():
    print("Function 1 started")
    await asyncio.sleep(2)
    print("Function 1 completed")

async def func2():
    print("Function 2 started")
    await asyncio.sleep(1)
    print("Function 2 completed")

async def func3():
    print("Function 3 started")
    await asyncio.sleep(3)
    print("Function 3 completed")

async def main():
    task1 = asyncio.create_task(func1())  # 创建任务1
    task2 = asyncio.create_task(func2())  # 创建任务2
    task3 = asyncio.create_task(func3())  # 创建任务3

    await asyncio.gather(task1, task2, task3)  # 并行执行所有任务

logger.info('开始')
asyncio.run(main())
logger.info('结束')
