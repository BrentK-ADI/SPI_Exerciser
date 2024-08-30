'''
Copyright © 2023 by Analog Devices, Inc.  All rights reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.

This software is provided on an “as is” basis without any representations,
warranties, guarantees or liability of any kind.

Use of the software is subject to the terms and conditions of the
Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
'''
import abc

class ISPI:
    '''
    Interface class for defining SPI bus connections
    '''

    @abc.abstractclassmethod
    def ReadWrite(self, xmit: list) -> list:
        '''
        Performs a SPI Read/Write Transaction

        :param xmit: List of bytes to transmit
        :return: List of bytes received, will be same length as xmit
        '''
        pass

    @abc.abstractclassmethod
    def Read(self, count: int) -> list:
        '''
        Performs a SPI Read Only Transaction

        :param count: Number of bytes to read
        :return: List of bytes read
        '''
        pass

    @abc.abstractclassmethod
    def Write(self, xmit: list) -> int:
        '''
        Performs a SPI Write Only Transaction

        :param xmit: List of bytes to transmit
        :return: Number of bytes transmitted
        '''
        pass

    @abc.abstractclassmethod
    def Cleanup(self) -> None:
        '''
        Cleans up any open resources
        '''
        pass

    @abc.abstractclassmethod
    def SetMode(self, mode: int) -> None:
        '''
        Sets the SPI mode (Phase/Polarity) of the bust

        :param mode: Mode to set (0-3)
        '''
        pass

    @abc.abstractclassmethod
    def SetSpeed(self, speed: int) -> None:
        '''
        Sets the SPI bus speed in Hz

        :param speed: Clock speed in Hz
        '''
        pass