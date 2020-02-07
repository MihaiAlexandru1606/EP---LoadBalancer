import requests
from threading import *
import random
import numpy
import time
import matplotlib.pyplot as plt
import numpy as np

from load_balancing_politicy import *
from constant import *


class MyThread(Thread):

    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self) -> None:
        for _ in range(10):
            print(str(self.id) + " " + str(requests.get("http://0.0.0.0:5000/work/us/0").text))


def run_test(scheduler, list_response_time, list_work_time, list_time):
    start_time = time.time()
    scheduler.start()
    scheduler.wait_to_finish()
    end_time = time.time()
    t = end_time - start_time

    list_response_time.append(scheduler.get_total_response_time())
    list_work_time.append(scheduler.get_total_work_time())
    list_time.append(t)


def draw_graph(inp, r: list, n: list, u: list, w: list, up: list, label_y, title):
    n_groups = len(inp)
    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.05
    opacity = 0.8

    rects1 = plt.bar(index, tuple(r), bar_width,
                     alpha=opacity,
                     color='b',
                     label='RandomSchedule')

    rects2 = plt.bar(index + bar_width, tuple(n), bar_width,
                     alpha=opacity,
                     color='g',
                     label='NaturalsSchedule')

    rects2 = plt.bar(index + 2 * bar_width, tuple(u), bar_width,
                     alpha=opacity,
                     color='y',
                     label='UniformWorkScheduler')

    rects2 = plt.bar(index + 3 * bar_width, tuple(w), bar_width,
                     alpha=opacity,
                     color='r',
                     label='WeightedScheduler')

    rects2 = plt.bar(index + 4 * bar_width, tuple(up), bar_width,
                     alpha=opacity,
                     color='m',
                     label='UniformWorkSchedulerParallel')

    plt.xlabel('Number request')
    plt.ylabel(label_y)
    plt.title(title)

    plt.xticks(index + bar_width, ('10', '50', '100', '200', '250', '300', '400', '500', '1000'))
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    inp = [10, 50, 100, 200, 250, 300, 400, 500, 1000]

    response_time_RandomSchedule = []
    work_time_RandomSchedule = []
    real_time_RandomSchedule = []

    response_time_NaturalsSchedule = []
    work_time_NaturalsSchedule = []
    real_time_NaturalsSchedule = []

    response_time_UniformWorkScheduler = []
    work_time_UniformWorkScheduler = []
    real_time_UniformWorkScheduler = []

    response_time_WeightedScheduler = []
    work_time_WeightedScheduler = []
    real_time_WeightedScheduler = []

    response_time_UniformWorkSchedulerParallel = []
    work_time_UniformWorkSchedulerParallel = []
    real_time_UniformWorkSchedulerParallel = []

    for i in inp:
        run_test(RandomSchedule(info_machines, i), response_time_RandomSchedule, work_time_RandomSchedule,
                 real_time_RandomSchedule)

        run_test(NaturalsSchedule(info_machines, i), response_time_NaturalsSchedule, work_time_NaturalsSchedule,
                 real_time_NaturalsSchedule)

        run_test(UniformWorkScheduler(info_machines, i), response_time_UniformWorkScheduler,
                 work_time_UniformWorkScheduler, real_time_UniformWorkScheduler)

        run_test(WeightedScheduler(info_machines, i), response_time_WeightedScheduler, work_time_WeightedScheduler,
                 real_time_WeightedScheduler)

        run_test(UniformWorkSchedulerParallel(info_machines, i), response_time_UniformWorkSchedulerParallel,
                 work_time_UniformWorkSchedulerParallel,
                 real_time_UniformWorkSchedulerParallel)

    draw_graph(inp, response_time_RandomSchedule, response_time_NaturalsSchedule, response_time_UniformWorkScheduler,
               response_time_WeightedScheduler, response_time_UniformWorkSchedulerParallel, "Time (ms)",
               "Response Time")

    draw_graph(inp, work_time_RandomSchedule, work_time_NaturalsSchedule, work_time_UniformWorkScheduler,
               work_time_WeightedScheduler, work_time_UniformWorkSchedulerParallel, "Time (ms)",
               "Work Time")

    draw_graph(inp, real_time_RandomSchedule, real_time_NaturalsSchedule, real_time_UniformWorkScheduler,
               real_time_WeightedScheduler, real_time_UniformWorkSchedulerParallel, "Time (s)",
               "Real Time")
