from daqhats import mcc152, HatError, HatIDs, hat_list

# create hat instance for rotary encoder
re = mcc152(1)

try:
    while True:
        position = re.dio_input_read_port()
        print("{0} : {0:08b}".format(position))
except KeyboardInterrupt:
    pass
