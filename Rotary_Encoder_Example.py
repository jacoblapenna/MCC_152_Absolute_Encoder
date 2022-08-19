from daqhats import mcc152, HatError, HatIDs, hat_list, DIOConfigItem

# create hat instance for rotary encoder
re = mcc152(1)
re.dio_reset()
re.dio_config_write_port(DIOConfigItem.INPUT_INVERT, 255)
last_pos = None

def g2b(num):
    num ^= num >> 4
    num ^= num >> 2
    num ^= num >> 1
    return num

g2b_hashmap = {g : g2b(g) for g in range(256)}

try:
    while True:
        pos = re.dio_input_read_port()
        bcd = g2b_hashmap(pos)
        if bcd == last_pos:
            pass
        else:
            print(f"{str(bcd).ljust(3)}" + " : {0:08b}".format(pos))
            last_pos = bcd
except KeyboardInterrupt:
    pass
