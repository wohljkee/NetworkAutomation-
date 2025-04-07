import paramiko

hostname = "192.168.102.2"
port = 22
username = "admin"
password = "password"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, port=port, username=username, password=password)

in_, out, err = ssh.exec_command('show version')

print(out.read().decode())
print(err.read().decode())
# in_.write('show version')
