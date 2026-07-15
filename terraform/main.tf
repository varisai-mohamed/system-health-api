resource "docker_image" "app" {

  name = var.image_name

  build {
    context = ".."
    dockerfile = "Dockerfile"
  }

  keep_locally = true

}

resource "docker_container" "app" {

  name = var.container_name
  image = docker_image.app.image_id

  restart = "unless-stopped"

  ports {
    internal = 8000
    external = 8000
  }

  volumes {
    host_path      = abspath(var.generated_graphs_path)
    container_path = "/app/generated_graphs"
  }

  volumes {
    host_path      = abspath(var.logs_path)
    container_path = "/app/logs"
  }    

}

