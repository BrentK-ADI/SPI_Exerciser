'''
Copyright © 2023 by Analog Devices, Inc.  All rights reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.

This software is provided on an “as is” basis without any representations,
warranties, guarantees or liability of any kind.

Use of the software is subject to the terms and conditions of the
Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
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