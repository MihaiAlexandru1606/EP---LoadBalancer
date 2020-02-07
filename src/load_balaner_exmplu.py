from load_balancing_politicy import *
import sys
from constant import *

if __name__ == '__main__':
    number_request = int(sys.argv[1])

    print("*************** RandomSchedule ***************")
    RandomSchedule(info_machines, number_request)
    print("Finish")
    print()
    print()

    print("*************** NaturalsSchedule ***************")
    NaturalsSchedule(info_machines, number_request)
    print("Finish")
    print()
    print()

    print("*************** UniformWorkScheduler ***************")
    UniformWorkScheduler(info_machines, number_request)
    print("Finish")
    print()
    print()

    print("*************** WeightedScheduler ***************")
    WeightedScheduler(info_machines, number_request)
    print("Finish")
    print()
    print()

    print("*************** UniformWorkSchedulerParallel ***************")
    UniformWorkSchedulerParallel(info_machines, number_request)
    print("Finish")
    print()
    print()