## webapp.tf
## ## Spec
## https://www.terraform.io/docs/configuration/syntax.html


resource "kubernetes_service" "quotes-webapp" {
  metadata {
    name = "quotes-webapp"
  }
  spec {
    selector = {
      app = "quotes-webapp"
      tier = "frontend"
    }

    port {
      port = 8080
      target_port = 8080
    }

    cluster_ip = "None"
  }
}


resource "kubernetes_deployment" "quotes-webapp" {
  metadata {
    name = "quotes-webapp"
    labels = {
      app = "quotes-webapp"
    }
  }

  spec {
    replicas = 2
    strategy {
      type = "Recreate"
    }

    selector {
      match_labels = {
        app = "quotes-webapp"
        tier = "frontend"
      }
    }

    template {
      metadata {
        labels = {
          app = "quotes-webapp"
          tier = "frontend"
        }
      }
      spec {
        container {
          name = "quotes-webapp"
          image = "${var.image_name}:${var.image_tag}"
          image_pull_policy = "Never"

          port {
            container_port = 8080
          }

          env {
            name = "GUNICORN_LOG_LEVEL"
            value = var.gunicorn_log_level
          }
        }
      }
    }
  }
}
