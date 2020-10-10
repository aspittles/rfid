#!/usr/bin/env python3

import subprocess

"""Get the core temperature.
Run a shell script to get the core temp and parse the output.
Raises:
  RuntimeError: if response cannot be parsed.
Returns:
  float: The core temperature in degrees Celsius.
"""
output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
temp_str = output.stdout.decode()
print ('Temp: ' + temp_str.split('=')[1].split('\'')[0])
# print output # float(temp_str.split('=')[1].split('\'')[0])


