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
import random
from IExerciser import IExerciser
from ISPI       import ISPI

#Registers with fixed data values
# Reg: Value
FIXED_REG_VALUES = { 0x00: 0xAD,
                     0x01: 0x1D,
                     0x02: 0xED }

class Exerciser_ADXL355(IExerciser):
    def __init__(self) -> None:
        super().__init__()

    def RunExercise(self, iface: ISPI ) -> float:
        '''
        Runs the ADXL355 Exercises.
        Reads the fixed register values as a single payload and individual bytes.
        Writes random data to the offset registers and reads back

        NOTE: Device operates in SPI Mode 0

        :param ISPI: SPI Interface to exercise against
        :return: Success rate
        '''        
        iface.SetMode(0)

        test_count = 0
        success_count = 0

        random.seed()

        #for the ADXL355, Address is bits 7:1 and Bit 0 is R / Wn

        for iters in range(0, 50): #arbitrarily 50 iterations
            #read DEVID_AD, DEVID_MST and PARTID As a group, then individually
            test_count += 1
            msg = [ 0x01, 0x00, 0x00, 0x00, 0x00 ]
            result = iface.ReadWrite(msg)
            logging.info('Received %s' % str(result))

            if ((result[1] == FIXED_REG_VALUES[0x00]) and 
                (result[2] == FIXED_REG_VALUES[0x01]) and 
                (result[3] == FIXED_REG_VALUES[0x02])):
                success_count += 1
            else:
                logging.warning('Expected 0x%02X 0x%02X 0x%02X, got %s' % 
                            (FIXED_REG_VALUES[0x00], FIXED_REG_VALUES[0x01],
                             FIXED_REG_VALUES[0x02], str(result[1:4])))

            # Read the ID registers individual;y
            for reg_addr in FIXED_REG_VALUES:
                test_count += 1
                msg = [ (reg_addr << 1) | 0x1, 0x00 ]
                result = iface.ReadWrite(msg)
                logging.info('Received %s' % str(result))

                if (result[1] == FIXED_REG_VALUES[reg_addr]):
                    success_count += 1
                else:
                    logging.warning('Expected 0x%02X, got %s' % 
                            (FIXED_REG_VALUES[reg_addr], str(result[1])))

            #Generate some random data for the Offset Regs add address 0x1E
            rand_data = list(random.randbytes(6))
            msg = [0x1E << 1]
            msg.extend(rand_data) 
            logging.info('Writing: %s' % str(msg))
            iface.Write(msg)

            #Read the written data byte by byes
            for offset in range(0,6):
                test_count += 1
                msg = [((0x1E + offset) << 1) | 1, 0x00]
                result = iface.ReadWrite(msg)
                logging.info('Received %s' % str(result))
                if (result[1] == rand_data[offset]):
                    success_count += 1
                else:
                    logging.warning('Expected 0x%02X, got %s' % 
                            (rand_data[offset], str(result[1])))

        logging.info('%d Tests / %d Success' % (test_count, success_count))
        return float(success_count) / float(test_count)