import logging
from datetime import datetime, timedelta

import asyncio
import socks
from telethon import TelegramClient
from pytz import timezone

import config
from utils import create_human_message


logging.basicConfig(level=logging.INFO, filename='logs.log')


async def stat(loop):
    proxy = (socks.SOCKS5, config.PROXY_HOST, config.PROXY_PORT, '', config.PROXY_USERNAME, config.PROXY_PASSWORD)
    now_day = datetime.now(tz=timezone('UTC')).replace(hour=0, minute=0, second=0)
    from_date = now_day - timedelta(days=config.COUNT_DAYS_FOR_ANALYZE)
    async with TelegramClient('statistics', config.API_ID, config.API_HASH, loop=loop, proxy=proxy) as client:
        await client.connect()
        all_statistics = {}
        async for dialog in client.iter_dialogs():
            logging.info('Сканим диалог {}'.format(dialog.name))
            dialog_statistics = {}
            count_questions = 0
            count_answers = 0
            limit = 100
            latest_chank_date = datetime.now(tz=timezone('UTC'))
            while latest_chank_date > from_date :
                async for message in client.iter_messages(dialog.entity, reverse=False, offset_date=latest_chank_date, limit=limit):
                    if message.date > from_date:
                        latest_chank_date = message.date
                    else:
                        latest_chank_date = from_date - timedelta(days=1)
                        break
                    if message.from_id not in dialog_statistics:
                        user = await client.get_entity(message.from_id)
                        dialog_statistics[message.from_id] = {'username': user.username,
                                                              'last_name': user.last_name,
                                                              'first_name': user.first_name,
                                                              'latest_message_data': message.date,
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
                    if dialog_statistics[message.from_id]['latest_message_data'] < message.date:
                        dialog_statistics[message.from_id]['latest_message_data'] = message.date
                all_statistics[dialog.name] = {'detail_statistics': dialog_statistics,
                                               'count_questions': count_questions,
                                               'count_answers': count_answers}

        message = await create_human_message(all_statistics)
        try:
            await client.send_message(config.TELEGRAM_ADMIN_NAME, message)
        except BaseException as e:
            logging.error(e)
            logging.info(message)


if __name__ == "__main__":
    aio_loop = asyncio.get_event_loop()
    try:
        aio_loop.run_until_complete(stat(aio_loop))
    except RuntimeError:
        pass
    finally:
        if not aio_loop.is_closed():
            aio_loop.close()
