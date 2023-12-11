# Another way to do it without clearing the Axis
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time, datetime, sys

def relative_time(reference_time, current_time):
    t1 = time.strptime(reference_time.split(',')[0], '%H:%M:%S')
    t2 = time.strptime(current_time.split(',')[0], '%H:%M:%S')
    r1_time = datetime.timedelta(hours=t1.tm_hour, minutes=t1.tm_min, seconds=t1.tm_sec).total_seconds()
    r2_time = datetime.timedelta(hours=t2.tm_hour, minutes=t2.tm_min, seconds=t2.tm_sec).total_seconds()

    return r2_time - r1_time

def reformat_time(time_column, reference_time):
    for i in range(len(time_column)):
        time_column[i].loc = relative_time(reference_time, time_column[i])

    return time_column

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
ax1.plot([], [], color= '#0097A7', linewidth=2, marker='.')
ax2.plot([], [], color= '#F50057', linewidth=2, marker='.')

ax1.set_title('Current')
ax2.set_title('Temperature')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 100)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 100)

def animate(i, reference_time):
    try:
        data1 = pd.read_csv(sys.argv[1])
        x1 = data1['current_time']
        x1 = reformat_time(x1, reference_time)
        y1 = data1['Current']

        ax1.lines[0].set_data(x1, y1)
        xlim_low, xlim_high = ax1.get_xlim()
        ylim_low, ylim_high = ax1.get_ylim()

        ylim_low = max(ylim_low, y1.min()) - 5
        ylim_high = y1.max() + 5
        ax1.set_xlim(xlim_low, (x1.max() + 5))
        ax1.set_ylim(ylim_low, ylim_high)
    except:
        pass



    try:
        data2 = pd.read_csv(sys.argv[2])
        x2 = data2['current_time']
        x2 = reformat_time(x2, reference_time)
        y2 = data2['Temperature']

        ax2.lines[0].set_data(x2, y2)
        xlim_low, xlim_high = ax2.get_xlim()
        ylim_low, ylim_high = ax2.get_ylim()

        ylim_low = max(ylim_low, y2.min()) - 5
        ylim_high =y2.max() + 5
        ax2.set_xlim(xlim_low, (x2.max() + 5))
        ax2.set_ylim(ylim_low, ylim_high)
    except:
        pass



t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


#ani = FuncAnimation(fig, animate, fargs=(sys.argv[1], ), interval=1000)
ani = FuncAnimation(fig, animate, fargs=(current_time, ), interval=1000)

ax1.tick_params(axis='both', labelsize=10)
ax2.tick_params(axis='both', labelsize=10)
ax1.title.set_size(10)
ax2.title.set_size(10)
plt.tight_layout()
plt.show()
