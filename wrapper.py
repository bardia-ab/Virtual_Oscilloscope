import os, platform

###################### Initialize ########################
work_directory = r'Results'
serial_port = 'COM12'
bitstream_path = r"bitstream\RO.bit"
##########################################################
seperator = '\\' if platform.system() == 'Windows' else '/'
project = bitstream_path.split(seperator)[-1].split('.')[0]
work_directory = os.path.join(work_directory, project)
try:
    os.mkdir(work_directory)
except FileExistsError:
    print('The folder Exists!')
    exit()

current_output = os.path.join(work_directory, 'current.csv')
temperature_output = os.path.join(work_directory, 'temperature.csv')

python = 'python' if platform.system() == 'Windows' else 'python3'
os.system(f'{python} main.py {serial_port} {bitstream_path} {current_output} {temperature_output}')