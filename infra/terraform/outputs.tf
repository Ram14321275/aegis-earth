output "kubernetes_cluster_name" {
  value       = google_container_cluster.primary.name
  description = "GKE Cluster Name"
}

output "database_connection_name" {
  value       = google_sql_database_instance.postgres.connection_name
  description = "Cloud SQL Instance Connection Name"
}

output "redis_host" {
  value       = google_redis_instance.cache.host
  description = "Redis Host IP"
}
