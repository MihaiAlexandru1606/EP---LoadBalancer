from threading import *
import requests
import json
from collections import namedtuple
from atomic_int import AtomicInt

InfoWorker = namedtuple("InfoWorker", ["region", "machine_id", "weighting", "max_request"])


class Worker(Thread):

    def __init__(self, region, machine_id, number_request):
        Thread.__init__(self)
        self.region = region
        self.machine_id = machine_id
        self.number_request = number_request
        self.url = "http://0.0.0.0:5000/work/" + str(self.region) + "/" + str(self.machine_id)
        self.total_response_time = 0
        self.total_work_time = 0

    def run(self) -> None:
        for _ in range(self.number_request):
            request = requests.get(self.url)
            j = request.json()
            self.total_response_time += int(j["response_time"])
            self.total_work_time += int(j["work_time"])
            print("Machine " + str(self.region) + " index " + str(self.machine_id) + " " + request.text)

    def get_total_response_time(self):
        return self.total_response_time

    def get_total_work_time(self):
        return self.total_work_time


class Worker2(Thread):

    def __init__(self, region, machine_id, number_request: AtomicInt):
        Thread.__init__(self)
        self.region = region
        self.machine_id = machine_id
        self.number_request = number_request
        self.url = "http://0.0.0.0:5000/work/" + str(self.region) + "/" + str(self.machine_id)
        self.total_response_time = 0
        self.total_work_time = 0

    def run(self) -> None:
        while True:
            if self.number_request.get_values() > 0:
                self.number_request.decrement_values()
                request = requests.get(self.url)
                j = request.json()
                self.total_response_time += int(j["response_time"])
                self.total_work_time += int(j["work_time"])
                print("Machine " + str(self.region) + " index " + str(self.machine_id) + " " + request.text)
            else:
                break

    def get_total_response_time(self):
        return self.total_response_time

    def get_total_work_time(self):
        return self.total_work_time
