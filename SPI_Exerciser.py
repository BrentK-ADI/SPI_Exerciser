'''
Copyright © 2023 by Analog Devices, Inc.  All rights reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.

This software is provided on an “as is” basis without any representations,
warranties, guarantees or liability of any kind.

Use of the software is subject to the terms and conditions of the
Clear BSD License ( https://spdx.org/licenses/BSD-3-Clause-Clear.html ).
'''
import argparse
import logging
import time
from Interfaces.SPI_spidev import SPI_spidev
from Interfaces.SPI_aardvark import SPI_aardvark
from Exercisers.Exerciser_AD5592r import Exerciser_AD5592r
from Exercisers.Exerciser_Loopback import Exerciser_Loopback
from Exercisers.Exerciser_ADXL355 import Exerciser_ADXL355


#Dictionary of possible Exerciser names and the classes
EXERCISER_DICT = { 'ad5592r': Exerciser_AD5592r,
                   'adxl355': Exerciser_ADXL355,
                   'loopback': Exerciser_Loopback }

#Dictionary of possible interface names and the classes
INTERFACE_DICT = { 'spidev': SPI_spidev,
                   'aardvark': SPI_aardvark}


def RunMain(args):
    '''
    Performs the actual main of the script.  Accepts the parsed command line
    arguments

    :param args: Parsed command line arguments
    '''
    #Bounds check the frequency span
    if(args.start_freq > args.end_freq):
        print('Start Frequency must be before End Frequency')
        return

    #Create the interface instance.
    if args.interface is SPI_spidev:
        #SPI Dev has extra arguments
        spi = SPI_spidev(args.bus_num, args.cs_num)
    else:
        spi = args.interface()

    #Create the exerciser instance
    if args.exerciser is Exerciser_Loopback:
        #Loopback has extra arguments
        exerciser = args.exerciser(args.lbmode)
    else:
        exerciser = args.exerciser()

    #Create a list of the frequencies to run
    freq_set = [*range(args.start_freq, args.end_freq, args.step_freq)]

    #Inclusive of end freq
    freq_set.append(args.end_freq)

    #probably dont need to do this, should be sorted from range + end_freq
    freq_set.sort()

    #Run all the frequencies
    for freq in freq_set:
        spi.SetSpeed(freq)
        result = exerciser.RunExercise(spi)
        print('Freq: %-9d Hz, Result: %.2f%%' % (freq, result * 100.0))

        #Delay if the user requested
        time.sleep(args.delay_ms / 1000.0)


def ArgCheckMode(value):
    '''
    Performs an argument check for the option SPI mode parameters. 0-3 are
    valide
    '''
    intval = int(value)
    if ((intval < 0) or (intval > 3)):
        raise argparse.ArgumentTypeError('%s is not a valid mode' % value)
    return intval

def ArgCheckInterface(value):
    '''
    Performs an argument check for the interface option. Use the INTERFACE_DICT
    for valid values
    '''
    if value.lower() not in INTERFACE_DICT:
        raise argparse.ArgumentTypeError('%s is not a valid interface' % value)
    return INTERFACE_DICT[str(value).lower()]

def ArgCheckExerciser(value):
    '''
    Performs an argument check for the exerciser option. Use the EXERCISER_DICT
    for valid values
    '''
    if value.lower() not in EXERCISER_DICT:
        raise argparse.ArgumentTypeError('%s is not a valid exerciser' % value)
    return EXERCISER_DICT[str(value).lower()]

def ArgCheckPositiveOrZero(value):
    '''
    Performs an argument check for values which need to be positive or 0
    '''
    intval = int(value)
    if intval < 0:
        raise argparse.ArgumentTypeError('%s is not Non-Negative' % value)
    return intval

def ArgCheckPositive(value):
    '''
    Performs an argument check for values which needs to be > 0
    '''
    intval = int(value)
    if intval <= 0:
        raise argparse.ArgumentTypeError('%s is not positive' % value)
    return intval


if __name__ == "__main__":
    #define the command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('--bus',   dest='bus_num',    type=ArgCheckPositive,
        default=0,       help='spidev bus number' )
    argParser.add_argument('--cs',      dest='cs_num',   type=ArgCheckPositive,
        default=0,       help='spidev chip select number' )
    argParser.add_argument('--start', dest='start_freq', type=ArgCheckPositiveOrZero,
        default=100000,  help='starting SPI clock frequency')
    argParser.add_argument('--end',   dest='end_freq',   type=ArgCheckPositive,
        default=1000000, help='Ending SPI clock frequency')
    argParser.add_argument('--step',  dest='step_freq',  type=ArgCheckPositive,
        default=50000,   help='Frequency step size')
    argParser.add_argument('--delay', dest='delay_ms', type=ArgCheckPositiveOrZero,
        default=0,       help='Delay (in ms) between frequency exercises')
    argParser.add_argument('--debug', dest='debug', action='store_true',
        help='Enabled debug output')
    argParser.add_argument('-e','--exerciser', dest='exerciser', type=ArgCheckExerciser,
        default='loopback', help='Select exerciser: ' + ','.join(EXERCISER_DICT.keys()))
    argParser.add_argument('-i','--interface', dest='interface', type=ArgCheckInterface,
        default='spidev', help='Select interface:' + ','.join(INTERFACE_DICT.keys()))
    argParser.add_argument('--lbmode', dest='lbmode',   type=ArgCheckMode,
        default=0,  help='SPI mode for the loopback exerciser')

    #Parse
    args = argParser.parse_args()

    #Setup logging
    if args.debug:
        logging.getLogger().disabled = False
        logging.getLogger().level = logging.DEBUG
    else:
        logging.getLogger().disabled = True

    RunMain(args)