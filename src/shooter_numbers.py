import collections


shooter_config = collections.namedtuple('ShooterConfig', ['mo', 'lester', 'hood'])

positions = {
    56: shooter_config(2000, 2000, 0),
    61: shooter_config(2000, 2100, 0),
    68: shooter_config(2300, 2000, 0),
    80: shooter_config(2350, 2000, 0),
    84: shooter_config(2400, 2100, 0),
    87: shooter_config(2400, 2200, 0),
    92: shooter_config(2459, 2175, 0),
    104: shooter_config(2500, 2100, 0),
    108: shooter_config(2586, 2300, 0),
    116: shooter_config(2600, 2250, 0),
    128: shooter_config(2990, 2600, 0),
    142: shooter_config(3163, 2750, 0),
    177: shooter_config(3000, 2761, 10),
    165: shooter_config(2900, 2700, 10)
}

positions_list = list(positions.keys())
