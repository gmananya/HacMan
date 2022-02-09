import subprocess, os, json
from subprocess import PIPE, Popen
from .models import Lab

def run_command(command):
    
    if type(command) is not list:
        command = str(command).strip()
        print("Running command: " + command)
        command = command.split(" ")
        command = [ x for x in command if x != '']
    print("command is :",command)
    
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout, stderr)
    return stdout, stderr

def get_lab_status(id=None):
    
    if id is None:
        command = ["docker", "ps", "-a", "--no-trunc" ,"--format={{json .}},"]
    else :
        lab = Lab.objects.get(id=id)
        lab_name = lab.slug_name
        command = ["docker", "ps", "-a", "--no-trunc",  '--filter', 'name='+lab_name ,"--format={{json .}},"]
        
    stdout, stderr = run_command(command)
    stdout = stdout.decode("utf-8")
    print("------------")
    stdout = stdout.strip()
    if not stdout :
        stdout = "[]"
    elif stdout[-1] == ",":
        stdout = stdout[:-1]
        stdout = "[" + stdout + "]"
    print(stdout)
        
    print("------------")
    
    data = json.loads(stdout)
    return data


def start_lab():
    pass 

def start_docker_compose_lab():
    pass 


def stop_lab():
    pass


def stop_docker_compose_lab():
    pass

# def get_lab_status():
#     pass

def get_docker_compose_lab_status():
    pass

def prune_all_labs():
    pass

def get_lab_containers(id):
    lab = Lab.objects.get(id=id)
    lab_name = lab.slug_name
    # lab_name = 'wordpress'
    # command = f"docker container ls -f name={lab_name}".format(lab_name) + " --format='[{{.ID}},{{.Image}},{{.Names}}]'"
    # command = f"docker container ls -f name={lab_name}".format(lab_name) + " --format='{{.ID}}'"
    command = ['docker', 'container', 'ls', '-f', 'name='+lab_name, '--format={"ID":"{{ .ID }}", "Image": "{{ .Image }}", "Names":"{{ .Names }}"}']
    stdout, stderr = run_command(command)
    stdout = stdout.decode("utf-8")
    stdout = json.loads(stdout)
    return {"stdout": stdout, "error": stderr.decode("utf-8")}

