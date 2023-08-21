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