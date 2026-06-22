variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The region to deploy resources to"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "The deployment environment (staging/production)"
  type        = string
  default     = "production"
}

variable "cluster_name" {
  description = "The name of the GKE cluster"
  type        = string
  default     = "aegis-earth-cluster"
}

variable "db_password" {
  description = "The password for the PostgreSQL database"
  type        = string
  sensitive   = true
}
