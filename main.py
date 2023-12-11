import time, multiprocessing, os, sys

def read_current(read_current_path, serial_port, current_output):
    os.system(f'python {read_current_path} {serial_port} {current_output}')

def read_temp(prog_log_temp_path, bitstream_path, temp_output):
    os.system(f'vivado -mode batch -nolog -nojournal -source {prog_log_temp_path} -tclargs "{bitstream_path}" "{temp_output}"')


def live_plot(current_output, temp_output):
    os.system(f'python real_time.py {current_output} {temp_output}')

if __name__ == '__main__':
    read_current_path = os.path.join('.', os.path.join('src', 'read_current.py'))
    serial_port = sys.argv[1]
    current_output = sys.argv[3]

    prog_log_temp_path = os.path.join('.', os.path.join('src', 'prog_log_temp.tcl'))
    bitstream_path = sys.argv[2]
    temp_output = sys.argv[4]

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file = open(current_output, 'w+')
    file.close()
    file = open(temp_output, 'w+')
    file.close()

    P1 = multiprocessing.Process(target=read_current, args=[read_current_path, serial_port, current_output])
    P2 = multiprocessing.Process(target=read_temp, args=[prog_log_temp_path, bitstream_path, temp_output])
    P3 = multiprocessing.Process(target=live_plot, args=[current_output, temp_output])
    P1.start()
    P2.start()
    #time.sleep(30)
    P3.start()

