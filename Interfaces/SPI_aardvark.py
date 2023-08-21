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