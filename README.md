# Chuck Norris Quotes webapp

---

This is flask based quotes webapp.

## Tests

There is some tests available.

```shell script
make tests
```

## Deploy (K8s / Minikube)

Terraform used as IaC tool. Minikube (K8s) used as deploy environment.

 * `image_name` - pass image name
 * `image_tag` - pass image tag
 * `gunicorn_log_level` - enable verbose output (useful for debug)

### Setup description

 * nginx used as reverse proxy (1 replica); official nginx image used
 * gunicorn / flask webapp (2 replicas); official alpine image used (+python3 runtime; +webapp)

```shell script
## Build and deploy
make deploy
```

```shell script
## Destroy deployment
make terraform-destroy
```

## Open service in browser

```shell script

minikube service quotes-webapp-nginx
```

## Links

 * [Quotes API](https://api.chucknorris.io/)
 * [Terraform](https://www.terraform.io/)
