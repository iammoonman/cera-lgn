import random


def get_number(num_to_take):
    """Returns a non-overlapping random sampled number."""
    list_nums = [n for n in range(1000)]
    out = random.sample(list_nums, num_to_take)
    return random.choice(out)


def get_sampled_numbers(n_packs_requested: int, n_rares_in_sheet: int):
    """Returns a randomly sampled list of numbers range(0,n_rares) with reduced chance of repeats."""
    out = []
    # Takes split samples of the range to maintain the chance of duplicates.
    while len(out) < n_packs_requested:
        out += random.sample(
            range(n_rares_in_sheet),
            k=(min([max([(n_packs_requested * 41 // 43) - n_rares_in_sheet, 1]), n_rares_in_sheet])),
        )
    return out
