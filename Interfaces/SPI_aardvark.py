'''
Copyright © 2023 by Analog Devices, Inc.  All rights reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.

This software is provided on an “as is” basis without any representations,
warranties, guarantees or liability of any kind.

Use of the software is subject to the terms and conditions of the
Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
'''
import logging
import array
from ISPI import ISPI

class SPI_aardvark(ISPI):
    '''
    Implementation of the ISPI interface class using the aardvark package for
    the TotalPhase aardvark device
    '''

    def __init__(self, aardvard_id: int = 0) -> None:
        '''
        Class constructor. Opens and initializes the spidev device

        :param aardvard_id: Optional Aardvark serial number. 0 (default) will
                            select first found device
        '''
        super().__init__()

        #Import things here to provide better cross platform support
        global aa
        import aardvark_py as aa

        (num, ports, unique_ids) = aa.aa_find_devices_ext(16, 16)
        port = None
        dongle_id = aardvard_id
        if aardvard_id == 0 and len(unique_ids) > 0:
            port = ports[0]
            dongle_id = unique_ids[0]
        else:
            for i in range(0, len(unique_ids)):
                if unique_ids[i] == aardvard_id:
                    port = ports[i]
                    dongle_id = unique_ids[i]
                    break

        if port is None:
            raise Exception('Failed to find dongle: ' + str(dongle_id))
        self.__aardvark_handle = aa.aa_open(port)
        if (self.__aardvark_handle <= 0):
            raise Exception('Failed to open dongle: ' + str(dongle_id))
        else:
            logging.info('Using dongle with ID: ' + str(dongle_id) + "\n")

        #Make sure it is in SPI mode
        aa.aa_configure(self.__aardvark_handle, aa.AA_CONFIG_SPI_I2C)


    def ReadWrite(self, xmit: list) -> list:
        #The Aardvard API uses arrays, so convert between lists and arrays here
        xmit_array = array.array('B', xmit)
        return_array = aa.array_u08(len(xmit))
        aa.aa_spi_write(self.__aardvark_handle, xmit_array, return_array )
        return return_array.tolist()

    def Read(self, count: int) -> list:
        xmit = [0]*count
        return self.ReadWrite(xmit)

    def Write(self, xmit: list) -> int:
        return len(self.ReadWrite(xmit))

    def SetMode(self, mode: int) -> None:
        if mode == 0:
            aa.aa_spi_configure(self.__aardvark_handle, 0, 0, aa.AA_SPI_BITORDER_MSB)
        elif mode == 1:
            aa.aa_spi_configure(self.__aardvark_handle, 1, 0, aa.AA_SPI_BITORDER_MSB)
        elif mode == 2:
            aa.aa_spi_configure(self.__aardvark_handle, 0, 1, aa.AA_SPI_BITORDER_MSB)
        elif mode == 3:
            aa.aa_spi_configure(self.__aardvark_handle, 1, 1, aa.AA_SPI_BITORDER_MSB)

    def SetSpeed(self, speed: int) -> None:
        #The Aardvark API takes speed in kHz, so convert
        aa.aa_spi_bitrate(self.__aardvark_handle, int(speed / 1000))

    def Cleanup(self) -> None:
        aa.aa_close(self.__aardvark_handle)