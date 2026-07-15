output "container_name" {
  value = docker_container.app.name
}

output "container_id" {
  value = docker_container.app.id
}

output "image_id" {
  value = docker_image.app.image_id
}