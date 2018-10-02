from itertools import chain


def mix_result_round_robin(*iterables):
    return list(chain.from_iterable(zip(*iterables)))


def order_date_index(item):
    '''
    Returns the key for the Project/challenges order function
    First order the nearest events in the future
    After those, come the ongoing events
    Last the events from the past
    :param item:
    :return:
    '''
    from datetime import datetime, timedelta

    start_date = item['start_date'] and datetime.strptime(item['start_date'], "%Y-%m-%dT%H:%M:%SZ")
    end_date = item['end_date'] and datetime.strptime(item['end_date'], "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()
    ten_years = timedelta(days=3650)
    hundred_years = timedelta(days=36500)

    if end_date:
        # If there is an end date must distinguish event in the future from events in the past
        results = now-end_date \
            if (now-end_date).days <= 0 \
            else now+(now-end_date)+hundred_years
    else:
        # Inverse order for the ongoing projects the newest goes first
        results = now-(now-start_date)+ten_years

    return str(results)
