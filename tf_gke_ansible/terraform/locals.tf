# export GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token) # 1 Hr. Validity
locals {
  env="${terraform.workspace}"
  counts = {
    "default"=1
    "production"=2
  }
  disk_capacity = {
    "default"=10
    "production"=10
  }
  cpu_count = {
    "default"=2
    "production"=4
  }
  machine = {
    "default"="e2-standard-1"
    "production"="n2-standard-1" # Examle only value
  }
  credential_location = {
    "default"="/home/k2patel/github/interview/tf_gke_ansible/terraform/cred.json"
    "production"="/home/k2patel/github/production/cred.json" # Examle only value
  }
  service_account_name = {
    "default"="unqork@unqork-379417.iam.gserviceaccount.com"
    "production"="unqork-prod@unqork-379417.iam.gserviceaccount.com" # Examle only value
  }
  project_hr_id = {
    "default"="unqork-379417"
    "production"="unqork-prod" # Examle only value
  }
  cluster_hr_name = {
    "default"="unqork-demo"
    "production"="unqork-prod"
  }
  cluster_hr_region = {
    "default"="us-east1"
  }
  cluster_hr_zones = {
    "default"=["us-east1-b"]
    "production"="us-east1-b"
  }
  cluster_hr_zone = {
    "default"="us-east1-b"
    "production"="us-east1-b"
  }
  machine_type="${lookup(local.machine,local.env)}"
  count="${lookup(local.counts,local.env)}"
  credentials_file_path="${lookup(local.credential_location,local.env)}"
  service_account="${lookup(local.service_account_name,local.env)}"
  cluster_name="${lookup(local.cluster_hr_name,local.env)}"
  region="${lookup(local.cluster_hr_region,local.env)}"
  zones="${lookup(local.cluster_hr_zones,local.env)}"
  disksize="${lookup(local.disk_capacity,local.env)}"
  cpus="${lookup(local.cpu_count,local.env)}"
  project_id="${lookup(local.project_hr_id,local.env)}"
  zone="${lookup(local.cluster_hr_zone,local.env)}"
}