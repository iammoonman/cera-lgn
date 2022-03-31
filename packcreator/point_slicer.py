import random

def respawn_sections(max_len, min_len=6, size=121):
    """Splits numbers from 0 to the size variable into smaller blocks."""
    sheet = [i for i in range(size)]
    sections = []
    while sheet:
        point = random.choice(sheet)
        sec = []
        for n in range(0, random.randint(min_len, max_len)):
            try:
                sheet.remove((point + n) % size)
                sec.append((point + n) % size)
            except:
                sec = []
                break
        if len(sec) > 0:
            sections.append(sec)
    return sections


def get_section(number_to_take):
    """Returns an index which will not intersect with another index.

    Pickles sections of numbers from which the indexes are drawn."""
    import pickle

    try:
        with open("sections.pickle", "rb") as f:
            sections = pickle.load(f)
    except:
        sections = None
    try:
        section_chosen = random.choice(
            [s for s in sections if len(s) >= number_to_take]
        )
    except:
        sections = respawn_sections(
            number_to_take, min_len=number_to_take - 2
        ) + respawn_sections(number_to_take, min_len=number_to_take - 2)
        section_chosen = random.choice(
            [s for s in sections if len(s) >= number_to_take]
        )
    sections.remove(section_chosen)
    while len(section_chosen) > number_to_take:
        if random.random() > 0.5:
            section_chosen.pop()
        else:
            section_chosen = section_chosen[1:]
    with open("sections.pickle", "wb") as f:
        pickle.dump(sections, f)
    return section_chosen[0]


def get_number(num_to_take):
    """Returns a non-overlapping random sampled number."""
    import pickle

    try:
        with open("numberset.pickle", "rb") as f:
            list_nums = pickle.load(f)
    except:
        list_nums = [n for n in range(1000)]
    try:
        out = random.sample(list_nums, num_to_take)
    except ValueError:
        list_nums = [n for n in range(1000)]
        out = random.sample(list_nums, num_to_take)
    with open("numberset.pickle", "wb") as f:
        pickle.dump([n for n in list_nums if n not in out], f)
    return random.choice(out)

