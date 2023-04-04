provider "google" {
  credentials = file("${local.credentials_file_path}")
}

module "gke_auth" {
  source       = "terraform-google-modules/kubernetes-engine/google//modules/auth"
  depends_on   = [module.gke]
  project_id   = local.project_id
  location     = module.gke.location
  cluster_name = module.gke.name
}

resource "local_file" "kubeconfig" {
  content  = module.gke_auth.kubeconfig_raw
  filename = "kubeconfig-${local.env}"
}

module "gcp-network" {
  source       = "terraform-google-modules/network/google"
  project_id   = local.project_id
  network_name = "${var.network}-${local.env}"
  subnets = [
    {
      subnet_name   = "${var.subnetwork}-${local.env}"
      subnet_ip     = "10.10.0.0/16"
      subnet_region = var.region
    },
  ]
  secondary_ranges = {
    "${var.subnetwork}-${local.env}" = [
      {
        range_name    = var.ip_range_pods_name
        ip_cidr_range = "10.20.0.0/16"
      },
      {
        range_name    = var.ip_range_services_name
        ip_cidr_range = "10.30.0.0/16"
      },
    ]
  }
}

module "gke" {
  source            = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  project_id        = local.project_id
  name              = "${local.cluster_name}-${local.env}"
  regional          = false
  region            = var.region
  zones             = var.zones
  network           = module.gcp-network.network_name
  subnetwork        = module.gcp-network.subnets_names[0]
  ip_range_pods     = var.ip_range_pods_name
  ip_range_services = var.ip_range_services_name
  node_pools = [
    {
      name            = "${local.cluster_name}-pool"
      machine_type    = local.machine_type
      node_locations  = var.zone
      min_count       = local.count
      max_count       = local.count
      disk_size_gb    = local.disksize
      preemptible     = false
      auto_repair     = false
      auto_upgrade    = true
      service_account = local.service_account
    },
  ]
}
