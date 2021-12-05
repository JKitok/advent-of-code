def parse_to_groups(lines):
    # Parse group of lines (that are separated by newline) into groups
    lines = [line.strip() for line in lines]
    groups = []
    while len(lines):
        try:
            next_ = lines.index("")
        except ValueError:
            next_ = len(lines)
        groups.append(lines[:next_])
        lines = lines[next_ + 1 :]
    return groups
