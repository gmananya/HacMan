from django.db import models

# Create your models here.


def folder_path(self, filename):
    print(self)
    print(filename)
    return "compose_files/{0}/{1}".format(self.slug_name, filename)


class Lab(models.Model):

    status_choices = (
        ("STOPPED", "STOPPED"),
        ("CREATED", "CREATED"),
        ("STARTING", "STARTING"),
        ("STOPPING", "STOPPING"),
        ("STARTED", "STARTED"),
        ("DISABLED", "DISABLED"),
    )


    name = models.CharField(max_length=100) # uniuqe=True, no space in name
    slug_name = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    path = models.CharField(max_length=100, blank=True)
    ports = models.CharField(max_length=100, blank=True)
    container_id = models.CharField(max_length=30, blank=True) # increase length
    created_at = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=30, blank=True, choices=status_choices)
    current_status = models.CharField(max_length=30, blank=True)
    container_name = models.CharField(max_length=30, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    command = models.CharField(max_length=100, blank=True)
    is_docker_compose = models.BooleanField(default=False)
    lab_details = models.TextField(blank=True)
    docker_compose_file = models.FileField(upload_to=folder_path, blank=True)
    
    # image / logo / banner
    
    
    # Docker or docker-compose [done]
    # content to display after the command [NA]
    # docker-compose file [done]
    # difficulty
    
    def __str__(self):
        return self.name
    
    def get_container_details(self):
        from .utils import get_lab_containers, get_lab_status
        return get_lab_status(self.id)
    

    def update_container_details(self):
        from .utils import  get_lab_status
        import json
        containers = get_lab_status(self.id)
        ports = []
        container_id = []
        created_at = []
        status = []
        current_status = []
        container_name = []
        lab_details = []
        
        
        for container in containers:
            ports.append(container['Ports'])
            container_id.append(container['ID'])
            created_at.append(container['CreatedAt'])
            # status.append(container['Status'])
            current_status.append(container['Status'])
            container_name.append(container['Names'])
        
        self.lab_details = containers
        self.ports = json.dumps(ports)
        self.container_id = json.dumps(container_id)
        self.created_at = json.dumps(created_at)
        self.current_status = json.dumps(current_status)
        self.container_name = json.dumps(container_name)
        
        Lab.save(self)