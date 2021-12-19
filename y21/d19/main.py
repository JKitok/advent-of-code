import os
import itertools
import collections
import numpy as np

rotations = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for arr in itertools.permutations([[x, 0, 0], [0, y, 0], [0, 0, z]]):
                matrix = np.array(arr)
                if np.linalg.det(matrix) == 1:
                    rotations.append(matrix)


def detect_overlap(array1, array2):
    for matrix in rotations:
        new_array2 = np.matmul(matrix, array2.T).T
        diffs = collections.Counter()
        for a in array1:
            for b in new_array2:
                diff = a - b
                diffs[str(np.round(diff).astype(int).tolist())] += 1
        mc = diffs.most_common()[0]
        if mc[1] >= 12:
            return matrix, np.array(eval(mc[0]))
    else:
        return None, None


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    # Parse as numpy arrays
    start_idx = [i for (i, line) in enumerate(lines) if line.startswith("--")]
    sensors = []
    for start, end in zip(start_idx, [*start_idx[1:], len(lines) + 1]):
        data = lines[start + 1 : end - 1]
        sensors.append(
            np.fromstring(",".join(data), sep=",").astype(int).reshape((len(data), 3))
        )

    positions = {}
    checked = []
    # Assume sensor 0 is correct
    aligned_sensors = [sensors.pop(0)]
    positions[hash(str(aligned_sensors[0]))] = np.array([0, 0, 0])
    while len(sensors) > 0:
        for (_, arr1), (idx, arr2) in itertools.product(
            enumerate(aligned_sensors), enumerate(sensors)
        ):
            hash1 = hash(str(arr1))
            hash2 = hash(str(arr2))
            if (hash1, hash2) in checked:
                continue
            else:
                checked.append((hash1, hash2))
                matrix, diff = detect_overlap(arr1, arr2)
                if matrix is not None:
                    break
        else:
            raise ValueError
        aligned = sensors.pop(idx)
        corrected = (
            np.matmul(matrix, aligned.T).T
            + np.repeat(diff, aligned.shape[0], axis=0).reshape(3, aligned.shape[0]).T
        )
        aligned_sensors.append(corrected)
        positions[hash(str(corrected))] = diff
        print(len(sensors))

    unique_sensors = []
    for sensor in aligned_sensors:
        for row in sensor:
            if not any(np.sum(np.abs(row - u)) < 1 for u in unique_sensors):
                unique_sensors.append(row)

    max_distance = 0
    for d1, d2 in itertools.combinations(positions.values(), 2):
        distance = np.sum(np.abs(d1 - d2))
        if distance > max_distance:
            max_distance = distance

    print(f"Part 1: {len(unique_sensors)}")
    print(f"Part 2: {max_distance}")
