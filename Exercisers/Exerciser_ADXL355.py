'''
Copyright © 2023 by Analog Devices, Inc.  All rights reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.

This software is provided on an “as is” basis without any representations,
warranties, guarantees or liability of any kind.

Use of the software is subject to the terms and conditions of the
Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
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