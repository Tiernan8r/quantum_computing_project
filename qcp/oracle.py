import gates as g


# size = number of qubits
# target = specific numbered state we're going to look for
def single_target_oracle(size, target):

    not_placement = (2 ** size) - 1 - target
    t = pull_set_bits(not_placement)

    cz = g.control_z(size, [x for x in range(0, size-1)], size-1)
    selector = g.multi_gate(size, t, 'x')
    oracle = selector * cz
    oracle *= selector
    return oracle


# returns the list of bits that is set in number n
def pull_set_bits(n):
    bits = []
    count = 0
    while n:
        cond = n & 1
        if cond:
            bits.append(count)
        n >>= 1
        count += 1
    return bits


def diffusion(size):
    h = g.multi_gate(size, [i for i in range(0, size)], 'h')
    cz = g.control_z(size, [i for i in range(0, size - 1)], size - 1)
    x = g.multi_gate(size, [i for i in range(0, size)], 'x')
    diff = h * (x * (cz * (x * h)))
    return diff
