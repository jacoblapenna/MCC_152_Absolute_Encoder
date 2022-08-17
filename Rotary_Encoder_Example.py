from daqhats import mcc152, HatError, HatIDs, hat_list

# create hat instance for rotary encoder
re = mcc152(1)

try:
    while True:
        print(re.dio_input_read_tuple())
except KeyboardInterrupt:
    pass
