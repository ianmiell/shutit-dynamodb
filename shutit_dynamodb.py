import random
import string

from shutit_module import ShutItModule

class shutit_dynamodb(ShutItModule):


	def build(self, shutit):
		vagrant_image = shutit.cfg[self.module_id]['vagrant_image']
		vagrant_provider = shutit.cfg[self.module_id]['vagrant_provider']
		gui = shutit.cfg[self.module_id]['gui']
		memory = shutit.cfg[self.module_id]['memory']
		module_name = 'shutit_dynamodb_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
		shutit.send('rm -rf /tmp/' + module_name + ' && mkdir -p /tmp/' + module_name + ' && cd /tmp/' + module_name)
		shutit.send('vagrant init ' + vagrant_image)
		shutit.send_file('/tmp/' + module_name + '/Vagrantfile','''
Vagrant.configure(2) do |config|
  config.vm.box = "''' + vagrant_image + '''"
  # config.vm.box_check_update = false
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = ''' + gui + '''
    vb.memory = "''' + memory + '''"
    vb.name = "shutit_dynamodb"
  end
end''')
		shutit.send('vagrant up --provider virtualbox',timeout=99999)
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant')

		shutit.install('openjdk-7-jre')
		shutit.install('python-pip')
		shutit.send('pip install boto3')
		shutit.send('wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz')
		shutit.send('tar -zxvf dynamodb_local_latest.tar.gz')
		shutit.send('java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb &')
		shutit.send('cd /root')
		shutit.send_host_file('/root/MoviesCreateTable.py','MoviesCreateTable.py')
		shutit.send('python /root/MoviesCreateTable.py')
		shutit.send_host_file('/root/moviedata.json.xz','moviedata.json.xz')
		shutit.send('xz -d /root/moviedata.json.xz')
		shutit.send_host_file('/root/MoviesLoadData.py','MoviesLoadData.py')
		shutit.send('python /root/MoviesLoadData.py')
		shutit.send_host_file('/root/MoviesLoadData.py','MoviesLoadData.py')
		shutit.send('python /root/MoviesLoadData.py')
		shutit.send_host_file('/root/CreateItem.py','CreateItem.py')
		shutit.send('python /root/CreateItem.py')
		shutit.send_host_file('/root/ReadItem.py','ReadItem.py')
		shutit.send('python /root/ReadItem.py')
		shutit.send_host_file('/root/UpdateItem.py','UpdateItem.py')
		shutit.send('python /root/UpdateItem.py')
		shutit.send_host_file('/root/ConditionalUpdate.py','ConditionalUpdate.py')
		shutit.send('python /root/ConditionalUpdate.py')
		shutit.send_host_file('/root/DeleteItem.py','DeleteItem.py')
		shutit.send('python /root/DeleteItem.py')
		shutit.send_host_file('/root/QueryAll.py','QueryAll.py')
		shutit.send('python /root/QueryAll.py')
		shutit.send_host_file('/root/ScanMovie.py','ScanMovie.py')
		shutit.send('python /root/ScanMovie.py')
		shutit.send_host_file('/root/QueryMovie.py','QueryMovie.py')
		shutit.send('python /root/QueryMovie.py')
		shutit.pause_point('')

		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		shutit.get_config(self.module_id,'vagrant_image',default='ubuntu/precise64')
		shutit.get_config(self.module_id,'vagrant_provider',default='virtualbox')
		shutit.get_config(self.module_id,'gui',default='false')
		shutit.get_config(self.module_id,'memory',default='1024')

		return True

	def test(self, shutit):

		return True

	def finalize(self, shutit):

		return True

	def isinstalled(self, shutit):

		return False

	def start(self, shutit):

		return True

	def stop(self, shutit):

		return True

def module():
	return shutit_dynamodb(
		'docker_enterprise_checklist.shutit_dynamodb.shutit_dynamodb', 2052683392.0001,   
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup','shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)
