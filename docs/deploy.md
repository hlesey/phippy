# Deploy

## Kubernetes

```bash
kubectl apply -f kubernetes/

kubectl get pods
kubectl get svc
```

Access [http://phippy.clusterx.qedzone.ro](http://phippy.clusterx.qedzone.ro:30080).

## Locally with Docker-Compose

```bash
make build
make push
docker compose up
```

Access [http://localhost:8080](http://localhost:8080).
