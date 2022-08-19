from daqhats import mcc152, HatError, HatIDs, hat_list, DIOConfigItem

# create hat instance for rotary encoder
re = mcc152(1)
re.dio_reset()
# pull-up resistor inverts input
re.dio_config_write_port(DIOConfigItem.INPUT_INVERT, 255)
last_pos = None

def g2b(num):
    num ^= num >> 4
    num ^= num >> 2
    num ^= num >> 1
    return num

d_theta_degrees = 360/256
g2b_hashmap = {g : g2b(g) for g in range(256)}

try:
    while True:
        pos = re.dio_input_read_port()
        bcd = g2b_hashmap[pos]
        if bcd == last_pos:
            pass
        else:
            angle = str(round(bcd * d_theta_degrees, 5))
            theta_whole, theta_decimal = angle.split('.')
            s = "{0:08b}".format(pos)
            s += " : "
            s += f"{theta_whole.rjust(3)}."
            s += f"{theta_decimal.ljust(5)}"
            print(s)
            last_pos = bcd
except KeyboardInterrupt:
    pass
