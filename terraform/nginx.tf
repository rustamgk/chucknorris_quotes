## nginx.tf
## ## Spec
## https://www.terraform.io/docs/configuration/syntax.html


resource "kubernetes_service" "quotes-webapp-nginx" {
  metadata {
    name = "quotes-webapp-nginx"
  }
  spec {
    selector = {
      app = "quotes-webapp"
      tier = "frontend"
    }

    port {
      port = 80
      target_port = 80
    }


    ## BUG: Terraform unable to finish service creationg on Minikube
    ## External IP -> Pending
    ## quotes-webapp -> Still creating
    #type = "LoadBalancer"
    type = "NodePort"
  }
}


resource "kubernetes_deployment" "quotes-webapp-nginx" {
  metadata {
    name = "quotes-webapp-nginx"
    labels = {
      app = "quotes-webapp"
    }
  }

  spec {
    replicas = 1
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
          name = "quotes-webapp-nginx"
          image = "${var.image_name}-nginx:${var.image_tag}"
          image_pull_policy = "Never"

          port {
            container_port = 80
          }
        }
      }
    }
  }
}
