## main.tf
## ## Spec
## https://www.terraform.io/docs/configuration/syntax.html

provider "kubernetes" {
  version = "~> 1.11"
  config_context = "minikube"
}


variable "image_name" {
  description = "Docker image name"
  type = string
  default = "chucknorris_webapp"
}

variable "image_tag" {
  description = "Docker image tag"
  type = string
  default = "latest"
}

variable "gunicorn_log_level" {
  description = "Gunicorn log level"
  type = string
  default = "info"
}
