import os, platform, shutil
import time
from pathlib import Path

def create_folder(FolderPath):
    try:
        os.mkdir(FolderPath)
    except FileExistsError:
        shutil.rmtree(FolderPath)
        os.mkdir(FolderPath)

###################### Initialize ########################
serial_port = 'COM12'
project = 'bardia_RO'
bitstream_path = Path('bitstream') / project
result_path = Path('Results') / project
prog_log_temp_path = Path('src') / 'prog_log_temp.tcl'
blank_bitstream = Path('bitstream') / 'blank_zu9eg_jtag.bit'
runtime = 60 * 1
##########################################################
if not os.path.exists(str(result_path)):
    os.mkdir(str(result_path))


python = 'python' if platform.system() == 'Windows' else 'python3'
start = time.time()
os.system(f'vivado -mode batch -nolog -nojournal -source {str(prog_log_temp_path)} -tclargs "{str(blank_bitstream)}" "None"')
diff = time.time() - start
time.sleep(60 * 1 - diff)

for bitstream in bitstream_path.glob('*.bit'):
    create_folder(str(result_path / bitstream.stem))
    current_output = str(result_path /  bitstream.stem / 'current.csv')
    temperature_output = str(result_path /  bitstream.stem / 'temperature.csv')
    figure_output = str(result_path /  bitstream.stem / f'{bitstream.stem}.pdf')
    os.system(f'{python} main.py {serial_port} {str(bitstream.absolute())} {current_output} {temperature_output} {figure_output} {runtime}')

    print('********* Reset *********')
    start = time.time()
    os.system(f'vivado -mode batch -nolog -nojournal -source {str(prog_log_temp_path)} -tclargs "{str(blank_bitstream)}" "None"')
    diff = time.time() - start
    time.sleep(60 * 1 - diff)