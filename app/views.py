from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Lab 
import json, os
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404
from .utils import run_command, get_lab_status, get_lab_containers
# Create your views here.

def debug_info(request):
    labs = Lab.objects.all()
    data = []
    for lab in labs:
        data.append(lab.get_container_details())
    return JsonResponse(data, safe=False) 
    
def prune_containers(request):
    # command = "docker container stop $(docker container ls -aq)"
    # command = ["docker", "container", "stop", "$(docker", "container", "ls", "-aq)"]
    # stdout, stderr = run_command(command)
    
    # command = "docker container prune -f"
    # stdout, stderr = run_command(command)
    
    script_files = os.path.join(settings.BASE_DIR, 'scripts')
    prune = os.path.join(script_files, 'prune_containers.sh')
    
    command = "sh {}".format(prune)
    stdout, stderr = run_command(command)
    
    labs = Lab.objects.all()
    for lab in labs:
        lab.status = "STOPPED"
        lab.save()
    return JsonResponse({"status": "ok"})
    
def index(request):
    labs = Lab.objects.all()
    
    for lab in labs:
        lab.tags = lab.tags.split(",")
        try:
            lab.current_status = json.loads(lab.current_status)
            if lab.current_status:
                lab.current_status = lab.current_status[0]
            else :
                lab.current_status = ""
        except Exception as e:
            messages.error(request, "Error: {}".format(e))
        
        try:
            lab.ports = json.loads(lab.ports)
        except Exception as e:
            messages.error(request, "Error: {}".format(e))
        
        
        
        
    return render(request, 'labs/index.html', {'labs': labs})

def home(request):
    labs = Lab.objects.all()
    messages.success(request, "Success: This is the sample success Flash message.")
    # messages.error(request, "Error: This is the sample error Flash message.")
    # messages.info(request, "Info: This is the sample info Flash message.")
    # messages.warning(request, "Warning: This is the sample warning Flash message.")
    return render(request, 'labs/home.html', {'labs': labs})

def lab_details(request, id):
    lab = get_object_or_404(Lab, pk=id)
    
    return render(request, 'labs/lab_details.html', {'lab':lab})

def list_labs(request):
    data = list(Lab.objects.all().values())
    return JsonResponse(data, safe=False)

# def running_labs(request):
#     data = list(Lab.objects.filter(status='running').values())
#     return JsonResponse(data, safe=False)
#     # TODO: return only running labs
    
# def stopped_labs(request):
#     data = list(Lab.objects.filter(status='stopped').values())
#     return JsonResponse(data, safe=False)
#     # TODO: return only stopped labs
    
def start_lab(request, id):
    lab = Lab.objects.get(id=id)
    print(lab)
    
    lab.status = "STARTING"
    lab.save()
    
    if lab.is_docker_compose :
        compose_file_path = os.path.join(settings.BASE_DIR, 'media')
        compose_file_path += "/" 
        compose_file_path += lab.docker_compose_file.name
        command = str(lab.command).format(FILENAME = compose_file_path)
        stdout, stderr = run_command(command)
        messages.error(request, stderr.decode("utf-8"))
    else:
        command = str(lab.command)
        print(command)
        command = command.format(slug_name = lab.slug_name)
        print(command)
        stdout, stderr = run_command(command)
        if stderr and not lab.is_docker_compose:
            # re.search("The container name .* is already in use by container", text)
            #          ("Bind for .* failed: port is already allocated")
            #          ("No such container: .*")
            messages.error(request, stderr.decode("utf-8"))

            return JsonResponse({"error": str(stderr)}, status=500)
    lab.update_container_details()
    data = {}
    data['status'] = "started"
    # data['container_id'] = stdout.decode("utf-8")
    lab.status = "STARTED"
    
    stdout = stdout.decode('utf-8')
    # lab.container_id = stdout
    lab.save()
    return JsonResponse(Lab.objects.filter(id=id).values()[0])

def stop_lab(request, id):
    lab = Lab.objects.get(id=id)
    print(lab)
    lab.status = "STOPPING"
    lab.save()
    # command = lab.command
    # print("command is :",command)
    
    if lab.is_docker_compose :
        compose_file_path = os.path.join(settings.BASE_DIR, 'media')
        compose_file_path += "/" 
        compose_file_path += lab.docker_compose_file.name
        command = "docker-compose -f {} down".format(compose_file_path)
    
    else :
        
        container_ids = lab.container_id
        print("container_ids :",str(container_ids))
        container_ids = json.loads(container_ids)
        container_ids = " ".join(container_ids)
        command = f"docker stop {container_ids}"
    
    stdout, stderr = run_command(command)
    messages.error(request, stderr.decode("utf-8"))
    
    
    if stderr and not lab.is_docker_compose:
        print(stderr)
        messages.error(request, stderr.decode("utf-8"))
        
        return JsonResponse({"error": str(stderr)}, status=500)
    
    else :
        data = {}
        lab.status = "STOPPED"
        data['container_id'] = stdout.decode("utf-8")
        lab.container_id = ""
        data['status'] = "stopped"
        lab.save()
    lab.update_container_details()
    
        
    return JsonResponse(list(Lab.objects.filter(id=id).values())[0])