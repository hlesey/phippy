# Phippy
Simple tutorial to build and deploy a simple Python app in Kubernetes.


## Build a Docker image from existing Python source code and push it to Docker Hub. 

You need to replace DOCKER_HUB_USER with your Docker Hub username.
```
docker build -t <DOCKER_HUB_USER>/phippy .
docker push <DOCKER_HUB_USER>/phippy
```

## Launch the app using Docker

You can use the existing commands to build/push/run the app:

```
make build
make push
make run
```

## Test the app
```
make run
curl localhost:5000
```

## Scale up the app with Docker Compose
```
docker-compose up -d --scale web=5
```

## Deploy the app to Kubernetes
```
kubectl apply -f kubernetes/
```

## Check that the Pods and Services are created
```
kubectl get pods
kubectl get svc
```

## Get the NodePort for the web Service. Make a note of the port.
```
kubectl describe svc phippy
```

## Test the app by accessing the NodePort of one of the nodes.

```
kubectl get nodes
curl <NODE_IP>:<NODEPORT>
```

## Optional - deploy app via ingress

```
kubectl apply -f kubernetes/ingress
```

## Test the app by accessing the ingress name and port

```
kubectl get ingress
kubectl describe ingress phippy

curl http://phippy.local
