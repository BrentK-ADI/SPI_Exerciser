'''
Copyright © 2023 by Analog Devices, Inc.  All rights reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.

This software is provided on an “as is” basis without any representations,
warranties, guarantees or liability of any kind.

Use of the software is subject to the terms and conditions of the
Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
'''
import abc
from ISPI import ISPI

class IExerciser:
    '''
    Interface class for defining exerciser instances
    '''

    @abc.abstractclassmethod
    def RunExercise(self, iface: ISPI ) -> float:
        '''
        Runs the exercise and returns the success rate percentage
        :param iface:  SPI Inteface to run the exeriser
        :return: Success rate percentage (0.0-1.0)
        '''
        pass