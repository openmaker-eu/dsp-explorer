from itertools import izip, chain
def mix_result_round_robin(*iterables):
    return list(chain.from_iterable(izip(*iterables)))