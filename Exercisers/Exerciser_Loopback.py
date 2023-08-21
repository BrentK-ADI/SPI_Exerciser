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
