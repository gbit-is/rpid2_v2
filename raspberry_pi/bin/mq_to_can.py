from pystalk import BeanstalkClient
import time


can_channel="can"
sleep_time=0.1
default_can_id="foo"


def publish_can(can_data,can_id=default_can_id):
	print(can_id,can_data)
	#..... yeah, nothing here yet
	# still waiting on my TJA1050 chips


def monitor_mq():

	mq_client = BeanstalkClient('127.0.0.1', 11300)
	mq_client.watch(can_channel)


	while True:
		for job in mq_client.reserve_iter():
			msg = job.job_data.decode()
			publish_can(msg)
			mq_client.delete_job(job.job_id)
			time.sleep(sleep_time)




error_count=0

while True:
	try:
		monitor_mq()
	except Exception as e:
		error_count += 1
		print(e)

	if error_count > 5:
		time.sleep(1)
