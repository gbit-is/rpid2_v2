import os

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
	




