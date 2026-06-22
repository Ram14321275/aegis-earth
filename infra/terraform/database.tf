resource "google_sql_database_instance" "postgres" {
  name             = "${var.environment}-postgres"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-custom-2-8192"
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.vpc.id
    }
    backup_configuration {
      enabled = true
      start_time = "02:00"
      point_in_time_recovery_enabled = true
    }
  }
}

resource "google_sql_user" "users" {
  name     = "postgres"
  instance = google_sql_database_instance.postgres.name
  password = var.db_password
}

resource "google_redis_instance" "cache" {
  name           = "${var.environment}-redis"
  memory_size_gb = 2
  region         = var.region
  tier           = "STANDARD_HA"

  authorized_network = google_compute_network.vpc.id
}
