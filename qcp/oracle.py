import gates as g


# size = number of qubits
# target = specific numbered state we're going to look for
def single_target_oracle(size, target):
    not_placement = 2 ** size - target
    t = pull_set_bits(not_placement)
    cz = g.control_z(size, [x for x in range(1, size)], size)
    selector = g.multi_gate(size, t, 'x')
    oracle = selector * cz
    oracle *= selector
    return oracle


# returns the list of bits that is set in number n
def pull_set_bits(n):
    bits = []
    count = 1
    while n:
        cond = n & 1
        if cond:
            bits.append(count)
        n >>= 1
        count += 1
    return bits



