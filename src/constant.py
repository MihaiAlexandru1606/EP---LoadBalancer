from worker import InfoWorker

worker_asia_0 = InfoWorker(region="asia", machine_id=0, weighting=2, max_request=10)
worker_asia_1 = InfoWorker(region="asia", machine_id=1, weighting=2, max_request=10)
worker_us_0 = InfoWorker(region="us", machine_id=0, weighting=1, max_request=10)
worker_us_1 = InfoWorker(region="us", machine_id=1, weighting=1, max_request=10)
worker_emea_0 = InfoWorker(region="emea", machine_id=0, weighting=1, max_request=10)

info_machines = [worker_asia_0, worker_asia_1, worker_emea_0, worker_us_0, worker_us_1]
