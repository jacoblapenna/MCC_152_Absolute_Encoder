from daqhats import mcc152, HatError, HatIDs, hat_list

# create hat instance for rotary encoder
re = mcc152(1)
re.dio_reset()
last_position = None

try:
    while True:
        position = re.dio_input_read_port()
        if position == last_position:
            pass
        else:
            print(f"{str(position).ljust(3)}" + " : {0:08b}".format(position))
            last_position = position
except KeyboardInterrupt:
    pass
