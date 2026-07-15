variable "container_name" {
  description = "Container name"
  type = string
  default = "system-health-api-container"
}

variable "image_name" {
  description = "Docker image name"
  type = string
  default = "system-health-api:latest"
}

variable "generated_graphs_path" {
  description = "Host path for generated graphs"
  type = string
  default = "../generated_graphs"
}

variable "logs_path" {
  description = "Host path for log files"
  type = string
  default = "../logs"
}