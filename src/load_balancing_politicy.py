from worker import *
import random


class RandomSchedule(object):

    def __init__(self, info_machines: list, number_request: int):
        self.no_worker = len(info_machines)
        self.workers = []
        number_request_remaining = number_request
        """
        pentru fiecare worker se acorda un numar random de requesturi de rezolvat, 
        numarul este in range-ul min : 1, max : number_request - no_machines + 1
        """
        for i in range(len(info_machines)):
            no_request = random.randint(1, number_request_remaining + i - self.no_worker + 1)
            number_request_remaining -= no_request
            worker = Worker(region=info_machines[i].region, machine_id=info_machines[i].machine_id,
                            number_request=no_request)
            self.workers.append(worker)

    def start(self):
        for worker in self.workers:
            worker.start()

    def wait_to_finish(self):
        for worker in self.workers:
            worker.join()

    def get_total_response_time(self):
        total_response_time = 0

        for worker in self.workers:
            total_response_time += worker.get_total_response_time()
        return total_response_time

    def get_total_work_time(self):
        total_work_time = 0

        for worker in self.workers:
            total_work_time += worker.get_total_work_time()

        return total_work_time


class NaturalsSchedule(object):
    """
    nu am gasit un nume mai bun, idea este ca se creaza un thread pt fiecare regiune si se fiecare executa un reguet,
    apoi, daca mai sunt request, executa si decrementeaza numarul de request-uri
    """

    def __init__(self, info_machines: list, number_request: int):
        self.no_worker = len(info_machines)
        self.workers = []
        self.no_request = AtomicInt(number_request)

        for info_machine in info_machines:
            worker = Worker2(region=info_machine.region, machine_id=info_machine.machine_id,
                             number_request=self.no_request)
            self.workers.append(worker)

    def start(self):
        for worker in self.workers:
            worker.start()

    def wait_to_finish(self):
        for worker in self.workers:
            worker.join()

    def get_total_response_time(self):
        total_response_time = 0

        for worker in self.workers:
            total_response_time += worker.get_total_response_time()
        return total_response_time

    def get_total_work_time(self):
        total_work_time = 0

        for worker in self.workers:
            total_work_time += worker.get_total_work_time()

        return total_work_time


class UniformWorkScheduler(object):
    """
    distribui nuamrul de request-uri pentru fiecare thread, care reprezinta o masina, in mod egal, un fel de RoundRobin
    """

    def __init__(self, info_machines: list, number_request: int):
        self.no_worker = len(info_machines)
        self.workers = []
        med = int(number_request / self.no_worker)
        remain = number_request - med * self.no_worker

        for info_machine in info_machines:
            worker = None
            if remain > 0:
                worker = Worker(region=info_machine.region, machine_id=info_machine.machine_id,
                                number_request=med + 1)
                remain -= 1
            else:
                worker = Worker(region=info_machine.region, machine_id=info_machine.machine_id,
                                number_request=med)
            self.workers.append(worker)

    def start(self):
        for worker in self.workers:
            worker.start()

    def wait_to_finish(self):
        for worker in self.workers:
            worker.join()

    def get_total_response_time(self):
        total_response_time = 0

        for worker in self.workers:
            total_response_time += worker.get_total_response_time()
        return total_response_time

    def get_total_work_time(self):
        total_work_time = 0

        for worker in self.workers:
            total_work_time += worker.get_total_work_time()

        return total_work_time


class WeightedScheduler(object):
    """
    distribui nuamrul de request-uri pentru fiecare thread, care reprezinta o masina, in functie de o pondera,
    acesta tine cont de timpul de raspuns, cum sunt apropioat cele mai bune au 2(adica cel mai mic) si cele mai slabe\
    masini au 1
    """

    def __init__(self, info_machines: list, number_request: int):
        self.no_worker = len(info_machines)
        self.workers = []
        all_weighting = 0

        for info_machine in info_machines:
            all_weighting += info_machine.weighting

        med = int(number_request / all_weighting)
        remain = number_request - med * all_weighting
        for info_machine in info_machines:
            worker = None
            if remain > 0:
                worker = Worker(region=info_machine.region, machine_id=info_machine.machine_id,
                                number_request=med * info_machine.weighting + 1)
                remain -= 1
            else:
                worker = Worker(region=info_machine.region, machine_id=info_machine.machine_id,
                                number_request=med * info_machine.weighting)
            self.workers.append(worker)

    def start(self):
        for worker in self.workers:
            worker.start()

    def wait_to_finish(self):
        for worker in self.workers:
            worker.join()

    def get_total_response_time(self):
        total_response_time = 0

        for worker in self.workers:
            total_response_time += worker.get_total_response_time()
        return total_response_time

    def get_total_work_time(self):
        total_work_time = 0

        for worker in self.workers:
            total_work_time += worker.get_total_work_time()

        return total_work_time


class UniformWorkSchedulerParallel(object):
    """
    la fel ca celalat, doar ca tine cont si de faptul ca o masina ar putea raspunda la mai multi clienti, astfel
    requesturile pentru o masina sunt timise de max_request / 2 client, variabila semnifica maxim de clienti la
    care poate sa rapunda in acelasi timp
    """

    def __init__(self, info_machines: list, number_request: int):
        self.no_worker = len(info_machines)
        self.workers = []
        med = int(number_request / self.no_worker)
        remain = number_request - med * self.no_worker

        for info_machine in info_machines:
            no_request_per_machine = 0

            if remain > 0:
                no_request_per_machine = med + 1
                remain -= 1
            else:
                no_request_per_machine = med

            no_client = int(info_machine.max_request / 2)
            med1 = int(no_request_per_machine / no_client)
            remain1 = no_request_per_machine - med1 * no_client

            for _ in range(no_client):
                worker = None

                if remain1 > 0:
                    remain1 -= 1
                    worker = Worker(region=info_machine.region, machine_id=info_machine.machine_id,
                                    number_request=med1 + 1)
                else:
                    worker = Worker(region=info_machine.region, machine_id=info_machine.machine_id,
                                    number_request=med1)

                self.workers.append(worker)

    def start(self):
        for worker in self.workers:
            worker.start()

    def wait_to_finish(self):
        for worker in self.workers:
            worker.join()

    def get_total_response_time(self):
        total_response_time = 0

        for worker in self.workers:
            total_response_time += worker.get_total_response_time()
        return total_response_time

    def get_total_work_time(self):
        total_work_time = 0

        for worker in self.workers:
            total_work_time += worker.get_total_work_time()

        return total_work_time
