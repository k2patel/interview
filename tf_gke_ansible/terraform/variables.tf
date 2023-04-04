variable "network" {
  description = "The VPC network created to host the cluster in"
  default     = "gke-network"
}
variable "subnetwork" {
  description = "The subnetwork created to host the cluster in"
  default     = "gke-subnet"
}
variable "ip_range_pods_name" {
  description = "The secondary ip range to use for pods"
  default     = "ip-range-pods"
}
variable "ip_range_services_name" {
  description = "The secondary ip range to use for services"
  default     = "ip-range-services"
}

variable "service-account-id" {
  description = "The ID of service account of GCP"
  default     = "serviceaccount-id"
}

variable "zones" {
  description = "The ID of service account of GCP"
  default     = ["us-east1-b"]
  type        = list
}

variable "zone" {
  description = "The ID of service account of GCP"
  default     = "us-east1-b"
}

variable "region" {
  description = "The ID of service account of GCP"
  default     = "us-east1"
}