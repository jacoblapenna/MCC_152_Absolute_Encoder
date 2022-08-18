from daqhats import mcc152, HatError, HatIDs, hat_list

# create hat instance for rotary encoder
re = mcc152(1)
re.dio_reset()
last_pos = None

def g2b(num):
    num ^= num >> 4
    num ^= num >> 2
    num ^= num >> 1
    return num

try:
    while True:
        pos = re.dio_input_read_port()
        g2b_pos = g2b(pos)
        if g2b_pos == last_pos:
            pass
        else:
            print(f"{str(g2b_pos).ljust(3)}" + " : {0:08b}".format(pos))
            last_pos = g2b_pos
except KeyboardInterrupt:
    pass
