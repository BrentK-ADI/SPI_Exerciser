'''
Copyright © 2023 by Analog Devices, Inc.  All rights reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.

This software is provided on an “as is” basis without any representations,
warranties, guarantees or liability of any kind.

Use of the software is subject to the terms and conditions of the
Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
'''
from ISPI import ISPI

class SPI_spidev(ISPI):
    '''
    Implementation of the ISPI interface class using the spidev package for
    the Linux spidev driver
    '''

    def __init__(self, bus_id: int, cs_id: int) -> None:
        '''
        Class constructor. Opens and initializes the spidev device

        :param bus_id: Bus number
        :param cs_id: CS number
        '''
        super().__init__()

        #import here so only tried if user creates an instance of spidev
        import spidev as sd

        self.__dev = sd.SpiDev()
        self.__dev.open(bus_id, cs_id)

    def ReadWrite(self, xmit: list) -> list:
        return self.__dev.xfer2(xmit)

    def Read(self, count: int) -> list:
        return self.__dev.readbytes(count)

    def Write(self, xmit: list) -> int:
        return self.__dev.writebytes(xmit)

    def SetMode(self, mode: int) -> None:
        self.__dev.mode = mode

    def SetSpeed(self, speed: int) -> None:
        self.__dev.max_speed_hz = speed

    def Cleanup(self) -> None:
        self.__dev.close()
