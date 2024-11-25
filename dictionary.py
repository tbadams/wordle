from typing import Optional

vowels = ['a', 'e', 'i', 'o', 'u']
vowels_and_y = vowels + ['y']

def contains_no(substr:str, targets) -> bool:
    return not any(i in targets for i in substr)

def len_is(substr:str, length:int) -> bool:
    return len(substr) == length

def present_count(count_dict, filter_fun):
    return list(
        sorted(
            [(key, value) for (key, value) in count_dict.items() if filter_fun(key)],
            key=lambda x: x[1],
            reverse = True
        )
    )

def format_count_item(kv:tuple[str, int]) -> str:
    return f"{kv[0]}:{kv[1]}"


input = open("words.txt", "r")
words = input.read().splitlines()
counts = {}
for word in words:
    last_char: Optional[str] = None
    for char in word:
        counts[char] = counts.get(char, 0) + 1
        if last_char:
            blend = f'{last_char}{char}'
            counts[blend] = counts.get(blend, 0) + 1
        last_char = char

counts_1 = present_count(counts, lambda key: len(key) == 1)
with open('counts1.txt', 'w') as f:
    for line in [format_count_item(kv) for kv in counts_1]:
        f.write(f"{line}\n")

counts_2 = present_count(counts, lambda key: len(key) == 2)
with open('counts2.txt', 'w') as f:
    for line in [format_count_item(kv) for kv in counts_2]:
        f.write(f"{line}\n")
        if not any(i in vowels for i in line):
            print(line)
