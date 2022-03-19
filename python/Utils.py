import logging
import os
from inspect import currentframe
from subprocess import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def border_msg(msg):
    """Print message inside the border

    >>> border_msg('hello')
        +-----+
        |hello|
        +-----+

    Args:
        msg (str): message to print inside border
    """
    row = len(msg)+4
    h = ''.join(['+'] + ['-' *row] + ['+'])
    result= h + '\n'"|  "+msg+"  |"'\n' + h
    print(bcolors.OKGREEN + result +  bcolors.ENDC)

def fixed_border_msg(msg):
    border = "="*51
    result = border + "\n" + msg + "\n" + border
    print(result)

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def processCmd(cmd, lineNumber = 0, quiet = 0):
    """This function is defined for processing of os command

    Args:
        cmd (str): The command to be run on the terminal
        lineNumber (int): The line number from where this function was invoked
        quiet (int, optional): Want to run the command in quite mode (Don't print anything) or print everything. Defaults to 0.

    Raises:
        RuntimeError: If the command failed then exit the program with exit code

    Returns:
        str: The full output of the command
    """
    output = '\n'
    print("="*51)
    print("[INFO]: Current working directory: {0}".format(os.getcwd()))
    print("[INFO]: {}#{} command:\n\t{}".format(os.path.basename(__file__), lineNumber, cmd)) # FIXME: now its always take filename as `Utils.py`. It should take the file name from where its called.
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=-1)
    for line in iter(p.stdout.readline, ''):
        output=output+str(line)
    p.stdout.close()

    if p.wait() != 0:
        raise RuntimeError("%r failed, exit status: %d" % (cmd, p.returncode))

    if (not quiet):
        print ('Output:\n   [{}] \n'.format(output))
    print("="*51)

    return output

class ColorLogFormatter(logging.Formatter):
     """A class for formatting colored logs.
     Reference: https://stackoverflow.com/a/70796089/2302094
     """

     # FORMAT = "%(prefix)s%(msg)s%(suffix)s"
    #  FORMAT = "\n[%(levelname)s] - [%(filename)s:#%(lineno)d] - %(prefix)s%(levelname)s - %(message)s %(suffix)s\n"
     FORMAT = "\n[%(levelname)s] - [%(filename)s:#%(lineno)d] - %(prefix)s%(message)s %(suffix)s\n"
    #  FORMAT = "\n%(asctime)s - [%(filename)s:#%(lineno)d] - %(prefix)s%(levelname)s - %(message)s %(suffix)s\n"

     LOG_LEVEL_COLOR = {
         "DEBUG": {'prefix': bcolors.OKBLUE, 'suffix': bcolors.ENDC},
         "INFO": {'prefix': bcolors.OKGREEN, 'suffix': bcolors.ENDC},
         "WARNING": {'prefix': bcolors.WARNING, 'suffix': bcolors.ENDC},
         "CRITICAL": {'prefix': bcolors.FAIL, 'suffix': bcolors.ENDC},
         "ERROR": {'prefix': bcolors.FAIL+bcolors.BOLD, 'suffix': bcolors.ENDC+bcolors.ENDC},
     }

     def format(self, record):
         """Format log records with a default prefix and suffix to terminal color codes that corresponds to the log level name."""
         if not hasattr(record, 'prefix'):
             record.prefix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get('prefix')

         if not hasattr(record, 'suffix'):
             record.suffix = self.LOG_LEVEL_COLOR.get(record.levelname.upper()).get('suffix')

         formatter = logging.Formatter(self.FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p' )
         return formatter.format(record)

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ColorLogFormatter())
logger.addHandler(stream_handler)
logger.setLevel( logging.DEBUG)

# log_level_map = {
#     "0": logging.WARNING,
#     "1": logging.INFO,
#     "2": logging.DEBUG
# }
