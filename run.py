import logging

import asyncio
import socks
from telethon import TelegramClient

import config


logging.basicConfig(level=logging.WARNING, filename='logs.log')


async def stat(loop):
    proxy = (socks.SOCKS5, config.PROXY_HOST, config.PROXY_PORT, '', config.PROXY_USERNAME, config.PROXY_PASSWORD)
    async with TelegramClient('statistics', config.API_ID, config.API_HASH, loop=loop, proxy=proxy) as client:
        await client.connect()
        all_statistics = {}
        async for dialog in client.iter_dialogs():
            dialog_statistics = {}
            count_questions = 0
            count_answers = 0
            async for message in client.iter_messages(dialog.entity, config.LIMIT_MESSAGES_FOR_ANALYZE):
                if message.from_id not in dialog_statistics:
                    user = await client.get_entity(message.from_id)
                    dialog_statistics[message.from_id] = {'username': user.username,
                                                          'last_name': user.last_name,
                                                          'first_name': user.first_name,
                                                          'questions': [],
                                                          'answers': []}
                if not message.message:
                    continue
                if '?' in message.message:
                    dialog_statistics[message.from_id]['questions'].append(message.message)
                    count_questions += 1
                else:
                    dialog_statistics[message.from_id]['answers'].append(message.message)
                    count_answers += 1
            all_statistics[dialog.name] = {'detail_statistics': dialog_statistics,
                                           'count_questions': count_questions,
                                           'count_answers': count_answers}

        message = ''
        for dialog_name, dialog in all_statistics.items():
            message += "Dialog '{}': questions - {}, answers - {}.\n".format(dialog_name,
                                                                             dialog['count_questions'],
                                                                             dialog['count_answers'])
        await client.send_message(config.TELEGRAM_ADMIN_NAME, message)


if __name__ == "__main__":
    aio_loop = asyncio.get_event_loop()
    try:
        aio_loop.run_until_complete(stat(aio_loop))
    except RuntimeError:
        pass
    finally:
        if not aio_loop.is_closed():
            aio_loop.close()
