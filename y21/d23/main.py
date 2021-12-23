import os
import copy

STOP_POSITIONS = [0, 1, 3, 5, 7, 9, 10]
BUCKET_IDX = [2, 4, 6, 8]
COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}


def to_position(top_row, bucket):
    return top_row + ":" + ",".join(bucket)


def from_position(string):
    top_row, buckets = string.split(":")
    buckets = buckets.split(",")
    return top_row, buckets


def get_home_bucket_position(amphipod, bucket, max_depth):
    if not all((bucket[i] in [" ", amphipod] for i in range(max_depth))):
        return -1
    else:
        return [i for i in range(max_depth) if bucket[i] == " "][-1]


def is_move_allowed(top_row, sidx, gidx):
    assert sidx != gidx
    if sidx < gidx:
        return all(top_row[i] == " " for i in range(sidx + 1, gidx + 1))
    else:
        return all(top_row[i] == " " for i in range(gidx, sidx))


def change_top(top_row, idx, value):
    return top_row[:idx] + value + top_row[idx + 1 :]


def change_bucket(buckets, bucket_idx, depth, value):
    new_buckets = copy.deepcopy(buckets)
    bucket = buckets[bucket_idx]
    new_buckets[bucket_idx] = bucket[:depth] + value + bucket[depth + 1 :]
    return new_buckets


def calculate_num_steps(sidx, target_idx, depth_start, depth_end):
    num_steps = abs(sidx - target_idx)
    if depth_start != -1:
        num_steps += depth_start + 1
    if depth_end != -1:
        num_steps += depth_end + 1
    return num_steps


def update(positions, visited, top_row, buckets, cost):
    new_position = to_position(top_row, buckets)
    if new_position in visited.keys():
        return positions
    if (not new_position in positions.keys()) or positions[new_position] > cost:
        positions[new_position] = cost
    return positions


def run(top_row, buckets):
    MAX_DEPTH = len(buckets[0])
    expected = " " * len(top_row) + ":" + ",".join(c * MAX_DEPTH for c in "ABCD")
    visited = {}
    positions = {to_position(top_row, buckets): 0}

    while True:
        # Get the position with lowest score thus far
        position, cost = sorted(positions.items(), key=lambda item: item[1])[0]
        visited[position] = cost
        if position == expected:
            break
        del positions[position]
        top_row, buckets = from_position(position)
        has_moved_in = False

        # Check if we can move into bucket from top row
        for sidx, amphipod in enumerate(top_row):
            if amphipod == " ":
                continue

            home_idx = "ABCD".index(amphipod)
            home_pos = get_home_bucket_position(amphipod, buckets[home_idx], MAX_DEPTH)
            if home_pos == -1:
                continue
            else:
                if is_move_allowed(top_row, sidx, BUCKET_IDX[home_idx]):
                    new_top = change_top(top_row, sidx, " ")
                    new_buckets = change_bucket(buckets, home_idx, home_pos, amphipod)
                    dcost = (
                        calculate_num_steps(sidx, BUCKET_IDX[home_idx], -1, home_pos)
                        * COSTS[amphipod]
                    )
                    positions = update(
                        positions, visited, new_top, new_buckets, cost + dcost
                    )
                    has_moved_in = True
        # Moving in will always be optimal, so don't care about other scenarios
        # if we have already moved
        if has_moved_in:
            continue
        # Go through each bucket and...
        for bidx, bucket in enumerate(buckets):
            # Ignore bucket if it is filled
            if all((bucket[i] == "ABCD"[bidx] for i in range(len(bucket)))):
                continue
            # Check if we can move directly into bucket
            try:
                amphipod = next((v for v in bucket if v != " "))
            except StopIteration:
                continue
            home_idx = "ABCD".index(amphipod)
            home_pos = get_home_bucket_position(amphipod, buckets[home_idx], MAX_DEPTH)
            if home_pos != -1 and bidx != home_idx:
                if is_move_allowed(top_row, BUCKET_IDX[bidx], BUCKET_IDX[home_idx]):
                    new_buckets = change_bucket(
                        buckets, bidx, bucket.index(amphipod), " "
                    )
                    new_buckets = change_bucket(
                        new_buckets, home_idx, home_pos, amphipod
                    )
                    dcost = (
                        calculate_num_steps(
                            BUCKET_IDX[bidx],
                            BUCKET_IDX[home_idx],
                            bucket.index(amphipod),
                            home_pos,
                        )
                        * COSTS[amphipod]
                    )
                    positions = update(
                        positions, visited, top_row, new_buckets, cost + dcost
                    )
                    has_moved_in = True

            # Check if we can move into open space
            for sidx in STOP_POSITIONS:
                if not has_moved_in and is_move_allowed(
                    top_row, BUCKET_IDX[bidx], sidx
                ):
                    new_top = change_top(top_row, sidx, amphipod)
                    new_buckets = change_bucket(
                        buckets, bidx, bucket.index(amphipod), " "
                    )
                    dcost = (
                        calculate_num_steps(
                            BUCKET_IDX[bidx],
                            sidx,
                            bucket.index(amphipod),
                            -1,
                        )
                        * COSTS[amphipod]
                    )
                    positions = update(
                        positions, visited, new_top, new_buckets, cost + dcost
                    )
        print(len(positions), min(positions.values()))
    return visited[expected]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    first_top_row = lines[1][1:-2].replace(".", " ")
    assert len(first_top_row) == 11
    start_buckets = [lines[2][i] + lines[3][i] for i in [3, 5, 7, 9]]
    # print(f"Part 1: {run(first_top_row, start_buckets)}")
    start_buckets = [
        v[0] + a + v[1] for (v, a) in zip(start_buckets, ["DD", "CB", "BA", "AC"])
    ]
    print(f"Part 2: {run(first_top_row, start_buckets)}")
