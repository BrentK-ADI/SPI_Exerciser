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
from IExerciser import IExerciser
from ISPI       import ISPI

class Exerciser_AD5592r(IExerciser):
    '''
    Exerciser for communication with AD5592.  Exericser performs device 
    configurations and readbacks to verify bus traffic
    '''
    def __init__(self) -> None:
        super().__init__()

    def RunExercise(self, iface: ISPI ) -> float:
        '''
        Runs the AD5592r Exercises.
        Configures the Output pin register to 0x01 - 0xFE, performs readback and
        verfies the data.

        NOTE: Device operates in SPI mode 1

        :param ISPI: SPI Interface to exercise against
        :return: Success rate
        '''
        iface.SetMode(1)

        test_count = 0
        success_count = 0

        #Avoid 0x00 and 0xFF as they presumably may give a false positive
        for pins in range(0x1, 0xFF):
            #increment the test count
            test_count += 1

            #Set Output Pins
            msg = [0x40, pins]
            iface.Write(msg)

            #Configure Register Readback
            msg = [0x38, 0x60]
            iface.Write(msg)
            
            #Read back the Output config
            result = iface.Read(2)
            logging.info('Received %s' % str(result))

            if result[1] == pins:
                success_count += 1
                logging.info('Valid Data 0x%02X' % result[1])
            else:
                logging.warning('Expected 0x%02X, got 0x%02X' % (pins, result[1]))

        logging.info('%d Tests / %d Success' % (test_count, success_count))

        return float(success_count) / float(test_count)