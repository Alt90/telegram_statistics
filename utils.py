from datetime import datetime
from pytz import timezone

import config


def pluralize(number, nouns):
    value = str(number)
    if str(value).endswith('1'):
        return '{} {}'.format(value, nouns[0])
    elif str(value)[-1:] in '234':
        return '{} {}'.format(value, nouns[1])
    else:
        return '{} {}'.format(value, nouns[2])


def human_timedelta(time_delta):
    secconds = time_delta.total_seconds()
    if secconds < 60:
        return '{0:.2f} c'.format(secconds)
    elif secconds < 3600:
        return '{0:.2f} м'.format(secconds/60)
    elif secconds < (3600*24):
        return '{0:.2f} ч'.format(secconds/3600)
    else:
        return '{0:.0f} д'.format(secconds / 3600/24)


async def create_human_message(statistics):
    message = 'Отчёт об общении в чатах {} за последние {}.\n'.format(config.LABL_NAME,
                                                                      pluralize(config.COUNT_DAYS_FOR_ANALYZE,
                                                                                ['день', 'дня', 'дней']))
    for dialog_name, dialog in statistics.items():
        message += "Группа {}:\n".format(dialog_name)
        for id, statistics in dialog['detail_statistics'].items():
            count_all_message = len(statistics['questions']) + len(statistics['answers'])
            sleep_time = datetime.now(tz=timezone('UTC')) - statistics['latest_message_data'].replace()
            message += "– {} {} (@{}) – {} , молчание {}\n".format(statistics['first_name'] or '',
                                                                   statistics['last_name'] or '',
                                                                   statistics['username'] or 'Неоприделён',
                                                                   pluralize(count_all_message,
                                                                             ['сообщение', 'сообщения', 'сообщений']),
                                                                   human_timedelta(sleep_time))
    return message