from googleapiclient.discovery import build


project_id = "sudip-try"
zone = "us-central1-a"


machine_type = "e2-medium"
boot_disk_size = 10 
name = "dstack-instance"

compute = build('compute', 'v1')

body = {
    "name": name,
    "machineType": f"zones/{zone}/machineTypes/{machine_type}",
    "disks": [
        {
      "boot": True,
    "initializeParams": {
      "sourceImage": "projects/debian-cloud/global/images/debian-10-buster-v20240417", 
      "diskSizeGb": "10"
    }
        }
    ],
}

network_interface = {
    "network": "global/networks/default",  
    "accessConfigs": [
        {
            "type": "ONE_TO_ONE_NAT",
            "name": "External NAT"
        }
    ]
}

body["networkInterfaces"] = [network_interface]

request = compute.instances().insert(project=project_id, zone=zone, body=body)
response = request.execute()


print(f"VM instance '{name}' created successfully.")