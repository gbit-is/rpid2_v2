import os
from pystalk import BeanstalkClient
mq_client = BeanstalkClient('127.0.0.1', 11300)



def init_common_config():

        import configparser
        config = configparser.ConfigParser()
        config.read('../etc/rpid2.conf')
        return config

def get_dir_path(dir_name):

	bin_dir = os.path.dirname(os.path.realpath(__file__))
	base_dir = os.path.abspath(os.path.join(bin_dir, os.pardir))
	lib_dir = os.path.abspath(os.path.join(base_dir,"libs"))
	etc_dir = os.path.abspath(os.path.join(base_dir,"etc"))

	dir_map = {
		"bin_dir"	:	bin_dir,
		"base_dir"	:	base_dir,
		"lib_dir"	:	lib_dir,
		"etc_dir"	:	etc_dir

	}
	
	return dir_map[dir_name]
	

def send_to_mq(message,channel="can"):
	with mq_client.using(channel) as inserter:
    		inserter.put_job(message)


def init_kvs():
        import dbm
        try:
                kvs = dbm.open('kvs', 'w')
        except:
                from recreateKVS import createKVS
                createKVS()
                kvs = dbm.open('kvs', 'w')

        return kvs



