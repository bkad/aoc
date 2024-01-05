import click
import sys


def count_valid_configurations(
    cache: dict[tuple[int, int, int, str], int],
    input: str,
    groups: list[int],
    group_idx: int = 0,
    curr_group_size: int = 0,
    idx: int = 0,
    idx_value: str = "",
) -> int:
    cache_key = (group_idx, curr_group_size, idx, idx_value)
    if cache_value := cache.get(cache_key):
        return cache_value
    while idx < len(input):
        if idx_value:
            char = idx_value
            idx_value = ""
        else:
            char = input[idx]
        match char:
            case "?":
                valid_hash = count_valid_configurations(
                    cache, input, groups, group_idx, curr_group_size, idx, "#"
                )
                valid_dot = count_valid_configurations(
                    cache,
                    input,
                    groups,
                    group_idx,
                    curr_group_size,
                    idx,
                    ".",
                )
                result = valid_hash + valid_dot
                cache[cache_key] = result
                return result
            case "#":
                curr_group_size += 1
                if group_idx == len(groups) or curr_group_size > groups[group_idx]:
                    cache[cache_key] = 0
                    return 0
                idx += 1
            case ".":
                if curr_group_size:
                    if group_idx == len(groups) or curr_group_size != groups[group_idx]:
                        cache[cache_key] = 0
                        return 0
                    group_idx += 1
                curr_group_size = 0
                idx += 1

    result = int(group_idx == len(groups))
    cache[cache_key] = result
    return result


def main(filename: str, multiplier) -> None:
    with open(filename, "r") as f:
        lines = f.readlines()

    valid_combos = 0
    with click.progressbar(lines) as bar:
        for line in bar:
            record, nums = line.split(" ")
            groups = [int(x) for x in nums.split(",")] * multiplier
            new_record = "?".join([record] * multiplier)
            valid = count_valid_configurations({}, new_record + ".", groups)
            valid_combos += valid
    return valid_combos


if __name__ == "__main__":
    print(main(sys.argv[1], int(sys.argv[2])))
    # print(count_valid_configurations("####.#...#...", [4, 1, 1]))
    # print(count_valid_configurations("##..##..##.", [2, 2, 2]))
    # print(count_valid_configurations("##..##..#.", [2, 2, 2]))
    # print(count_valid_configurations("#..##..##.", [2, 2, 2]))
    # print(count_valid_configurations("##.###..####.", [2, 3, 4]))
