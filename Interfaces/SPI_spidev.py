'''
 * Copyright (C) 2023 Analog Devices, Inc.
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *  - Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  - Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *  - Neither the name of Analog Devices, Inc. nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *  - The use of this software may or may not infringe the patent rights
 *    of one or more patent holders.  This license does not release you
 *    from the requirement that you obtain separate licenses from these
 *    patent holders to use this software.
 *  - Use of the software either in source or binary form, must be run
 *    on or directly connected to an Analog Devices Inc. component.
 *
 * THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT,
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, INTELLECTUAL PROPERTY RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
