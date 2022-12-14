from daqhats import mcc152, HatError, HatIDs, hat_list, DIOConfigItem, interrupt_callback_enable

from threading import Lock

class Encoder:

    def __init__(self, resolution=256):

        # instantiate DAQ
        self._mcc152 = mcc152(1) # update to your correct address here

        # create instance attributes
        self.direction = None # None, "CCW", or "CW"
        self.resolution = resolution
        self.rotations = 0
        self.d_theta_degrees = d_theta_degrees = 360/self.resolution
        self._g2b_hashmap = {g : self._g2b(g) for g in range(self.resolution)}
        self._lock = Lock()

        # set interupt callback
        interrupt_callback_enable(self._count_rev, self.direction)

        # initialize DAQ
        self._mcc152.dio_reset()
        self._mcc152.dio_config_write_port(DIOConfigItem.INPUT_INVERT, int(b"11111111", 2))
        self._mcc152.dio_config_write_port(DIOConfigItem.INPUT_LATCH, int(b"11111111", 2))
        self._mcc152.dio_config_write_port(DIOConfigItem.INT_MASK, int(b"01111111", 2))

        # get initial offset
        self._degrees_offset = self._bcd2angle(self._g2b_hashmap[self._mcc152.dio_input_read_port()])
        self.position = 0.0


    def _g2b(self, num):
        """
        Private method to convert a gray coded integer to a binary coded integer.
        """
        num ^= num >> 4
        num ^= num >> 2
        num ^= num >> 1
        return num


    def _bcd2angle(self, bcd):
        """
        Private method to convert a BCD integer to angular position.
        """
        return bcd * self.d_theta_degrees


    def _count_rev(self, direction):
        """
        Keep track of revolutions past BCD=255/0 point.
        """
        self._lock.acquire()
        pos = self._mcc152.dio_input_read_port()
        bcd = self._g2b_hashmap[pos]
        if bcd == 255:
            self.rotations -= 1
        elif bcd == 0:
            self.rotations += 1
        self._lock.release()


    def _show_angle(self):
        """
        Print the most recent angular position in a nice format.
        """
        print("{:.5f}".format(round(self.position, 5)).rjust(15))


    def _update_position(self, angle):
        """
        Update the encoder's angular position.
        """
        self._lock.acquire()
        if self.rotations < 0:
            self.position = self.rotations * 360 + angle - self._degrees_offset
        else:
            self.position = (angle + self.rotations * 360) - self._degrees_offset
        self._lock.release()
        self._show_angle()


    def track_rotation(self):
        """
        Track the encoder's location until KeyboardInterrupt.
        """
        last_pos = None
        try:
            while True:
                pos = self._mcc152.dio_input_read_port()
                angle = self._bcd2angle(self._g2b_hashmap[pos])
                if angle == last_pos:
                    pass
                else:
                    self._update_position(angle)
                    last_pos = angle
        except KeyboardInterrupt:
            return

if __name__ == '__main__':
    encoder = Encoder()
    encoder.track_rotation()
