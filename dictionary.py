vowels = ['a', 'e', 'i', 'o', 'u','y']

def present_count(count_dict, filter_fun):
    return list(
        sorted(
            [(key, value) for (key, value) in count_dict.items() if filter_fun(key)],
            key=lambda x: x[1],
            reverse = True
        )
    )

input = open("words.txt", "r")
words = input.read().splitlines()
counts = {}
for word in words:
    last_char = None
    for char in word:
        counts[char] = counts.get(char, 0) + 1
        if last_char:
            blend = f'{last_char}{char}'
            counts[blend] = counts.get(blend, 0) + 1
        last_char = char
counts_1 = present_count(counts, lambda key: len(key) == 1)

with open('counts1.txt', 'w') as f:
    for line in [f"{kv[0]}:{kv[1]}" for kv in counts_1]:
        f.write(f"{line}\n")

counts_2 = present_count(counts, lambda key: len(key) == 2)

with open('counts2.txt', 'w') as f:
    print("2 letter blends, no vowels:")
    for line in [f"{kv[0]}:{kv[1]}" for kv in counts_2]:
        f.write(f"{line}\n")
        if not any(i in vowels for i in line):
            print(line)



