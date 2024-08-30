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
import numpy
from IExerciser import IExerciser
from ISPI       import ISPI

class Exerciser_Loopback(IExerciser):
    '''
    Implementation of IExerciser for a loopback interface.
    This assumes MISO/MOSI is tied together, or an endpoint device that is
    repeating the input data in real time.
    '''
    def __init__(self, mode: int) -> None:
        '''
        Class constructor.

        :param mode: SPI Mode to use for the exercises
        '''
        super().__init__()
        self.__mode = mode

    def RunExercise(self, iface: ISPI) -> float:
        '''
        Runs the loopback exercises.
        For packet widths of 1-8 bytes, 50 iterations, generates random payloads
        of data and verifies all transmitted bytes are identially received

        :param iface: ISPI Interface to write over
        :return: Success rate
        '''

        test_count = 0
        success_count = 0

        random.seed()
        iface.SetMode(self.__mode)

        for width in range(1, 9):      #Do payloads of 1-8 bytes
            for iters in range(0, 50): #50 Iteractions per width
                test_count += 1

                #Generate the random payload
                msg = list(random.randbytes(width))

                #No guarantee the data wont be mangled by the SPI interface
                msg_orig = msg.copy()
                result = iface.ReadWrite(msg)

                logging.info('Wrote %s, Received %s' % (str(msg_orig), str(result)))

                if (numpy.array([msg_orig]) == numpy.array([result])).all():
                    success_count += 1
                    logging.info('Valid Data')
                else:
                    logging.warning('Expected: %s, Got: %s' % (str(msg_orig), str(result)))

        logging.info('%d Tests / %d Success' % (test_count, success_count))

        return float(success_count) / float(test_count)
