import time, multiprocessing, os, sys

def read_current(read_current_path, serial_port, current_output, runtime):
    os.system(f'python {read_current_path} {serial_port} {current_output} {runtime}')

def read_temp(prog_log_temp_path, bitstream_path, temp_output):
    os.system(f'vivado -mode batch -nolog -nojournal -source {prog_log_temp_path} -tclargs "{bitstream_path}" "{temp_output}"')


def live_plot(current_output, temp_output, figure_output, runtime):
    os.system(f'python real_time.py {current_output} {temp_output} {figure_output} {runtime}')

if __name__ == '__main__':
    read_current_path = os.path.join('.', os.path.join('src', 'read_current.py'))
    serial_port = sys.argv[1]
    current_output = sys.argv[3]

    prog_log_temp_path = os.path.join('.', os.path.join('src', 'prog_log_temp.tcl'))
    bitstream_path = sys.argv[2]
    temp_output = sys.argv[4]

    figure_output = sys.argv[5]
    runtime = sys.argv[6]

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file = open(current_output, 'w+')
    file.close()
    file = open(temp_output, 'w+')
    file.close()


    P1 = multiprocessing.Process(target=read_current, args=[read_current_path, serial_port, current_output, runtime])
    P2 = multiprocessing.Process(target=read_temp, args=[prog_log_temp_path, bitstream_path, temp_output])
    P3 = multiprocessing.Process(target=live_plot, args=[current_output, temp_output, figure_output, runtime])
    P1.start()
    P2.start()
    P3.start()

    time.sleep(int(runtime) + 10)

    P1.terminate()
    P2.terminate()
    P3.terminate()
    os.system('taskkill /IM vivado.exe /F')
