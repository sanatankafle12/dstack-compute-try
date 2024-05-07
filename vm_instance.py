from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

project_id = "sudip-try"
zone = "us-central1-a"

tpu_version = "v3-8"  # Desired TPU version (e.g., v3, v4)
tpu_cores = 8 

machine_type = "e2-micro"
boot_disk_size = 10
name = "dstack-instance-tpu"

compute = build('compute', 'v1')

body = {
  "name": name,
  "machineType": f"zones/{zone}/machineTypes/{machine_type}",
  "disks": [
    {
      "boot": True,
      "initializeParams": {
        "sourceImage": "projects/debian-cloud/global/images/debian-10-buster-v20240417",
        "diskSizeGb": str(boot_disk_size)  # Ensure disk size is a string
      }
    }
  ],
  "networkInterfaces": [
    {
      "network": "global/networks/default",
      "accessConfigs": [
        {
          "type": "ONE_TO_ONE_NAT",
          "name": "External NAT"
        }
      ]
    }
  ],
  "accelerators": [
    {
      "type": f"zones/{zone}/tpuTypes/tpu-{tpu_version}",
      "acceleratorCount": tpu_cores
    }
  ]
}

network_interface = body["networkInterfaces"][0] 

try:
  request = compute.instances().insert(project=project_id, zone=zone, body=body)
  response = request.execute()
  print(f"VM instance '{name}' created successfully.")
except HttpError as error:
  print(f"Error creating VM instance: {error.content}")