import logging
import sys

# creating a logging.logger instance and gigving it a name(myLogger)
logger = logging.getLogger("myLogger")

# Add a formatter
# This uses LogRecord attributes
# https://docs.python.org/3/library/logging.html#logrecord-attributes
formatter = logging.Formatter(fmt='%(name)s: %(asctime)s: %(levelno)s: %(message)s')

# add handler objects
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename='logs.text')
file_handler.setFormatter(formatter)

# Add handlers to the root logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# A function to test the logger
def division(numerator, denominator):
    try:
        return numerator / denominator
    except ZeroDivisionError:
        logger.error(f"Division by zero error with parameters: {numerator} / {denominator}")


if __name__ == "__main__":
    division(4, 0)