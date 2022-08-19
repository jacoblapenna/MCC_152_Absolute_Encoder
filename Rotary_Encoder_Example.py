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

try:
    while True:
        pos = re.dio_input_read_port()
        g2b(pos)
        if pos == last_pos:
            pass
        else:
            print(f"{str(pos).ljust(3)}" + " : {0:08b}".format(pos))
            last_pos = pos
except KeyboardInterrupt:
    pass
