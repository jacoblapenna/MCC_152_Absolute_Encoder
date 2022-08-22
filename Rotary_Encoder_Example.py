from daqhats import mcc152, HatError, HatIDs, hat_list, DIOConfigItem, interrupt_callback_enable

class Encoder:

    def __init__(self, resolution=256):

        # instantiate DAQ
        self._mcc152 = mcc152(1) # detect address first in production

        # create instance attributes
        self.direction = None # None, "CCW", or "CW"
        self.resolution = resolution
        self.rotations = 0
        self.d_theta_degrees = d_theta_degrees = 360/self.resolution
        self._g2b_hashmap = {g : self._g2b(g) for g in range(self.resolution)}

        # set interupt callback
        interrupt_callback_enable(self._count_rev, self.direction)

        # initialize DAQ
        self._mcc152.dio_reset()
        self._mcc152.dio_config_write_port(DIOConfigItem.INPUT_INVERT, int(b"11111111", 2))
        self._mcc152.dio_config_write_port(DIOConfigItem.INPUT_LATCH, int(b"11111111", 2))
        self._mcc152.dio_config_write_port(DIOConfigItem.INT_MASK, int(b"01111111", 2))


    def _g2b(self, num):
        """
        Private method to convert a gray coded integer to a binary coded integer.
        """
        num ^= num >> 4
        num ^= num >> 2
        num ^= num >> 1
        return num


    def _count_rev(self, direction):
        """
        One revolution occurs when the MSB goes high to low.
        This is a + rotation if
        """
        pos = self._mcc152.dio_input_read_port()
        if pos == 255:
            self.rotations -= 1
        elif pos == 0:
            self.rotations += 1
        print('-' * 6 + "{0:08b}".format(pos) + '-' * 6)


    def track_rotation(self):
        last_pos = None
        try:
            while True:
                pos = self._mcc152.dio_input_read_port()
                bcd = self._g2b_hashmap[pos]
                if bcd == last_pos:
                    pass
                else:
                    angle = str(round(bcd * self.d_theta_degrees, 5))
                    theta_whole, theta_decimal = angle.split('.')
                    s = "{0:08b}".format(pos)
                    s += " : "
                    s += f"{str(self.rotations).rjust(5)} + "
                    s += f"{theta_whole.rjust(3)}."
                    s += f"{theta_decimal.ljust(5)}"
                    print(s)
                    last_pos = bcd
        except KeyboardInterrupt:
            return

if __name__ == '__main__':
    encoder = Encoder()
    encoder.track_rotation()
