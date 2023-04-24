import paramiko

# list of dictionaries, where each dictionary contains the IP address, username, and password for each Raspberry Pi computer
devices = [
    {"ip": "openauto", "username": "pi", "password": "Silverado05!"},
    {"ip": "openauto2", "username": "pi", "password": "Silverado05!"},
    {"ip": "dztesterpi", "username": "pi", "password": "Silverado05!"}
]

# loop through each device and establish an SSH connection
for device in devices:
    # create a new SSH client
    ssh = paramiko.SSHClient()
    # automatically add the server's host key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to the remote server
    ssh.connect(device["ip"], username=device["username"], password=device["password"])
    # issue the shutdown command
    ssh.exec_command("sudo shutdown now")
    # close the SSH connection
    ssh.close()
