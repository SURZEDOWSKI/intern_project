#this file is used only to test if messages work correctly!

import asyncio

import aio_pika

async def consume():
    connection = await aio_pika.connect('amqp://guest:guest@Rabbitmq')

    async with connection:
        queue_name = 'users_queue'
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

if __name__ == '__main__':
    asyncio.run(consume())