# Install a Kubernetes cluster with K3s

*NOTE: This instructions are a condensed version of the [official instructions](https://docs.k3s.io/quick-start).*

## K3s quick-start

Execute the following command will create a single-node Kubernetes cluster:

	curl -sfL https://get.k3s.io | sh -

The command also installs kubectl and creates a kubeconfig file (/etc/rancher/k3s/k3s.yaml). 

To be able to run k3s commands without sudo do the following:

	mkdir -p .kube && sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config && sudo chown $USER ~/.kube/config && chmod 600 ~/.kube/config && export KUBECONFIG=~/.kube/config

Test:

	kubectl get node

## Accessing Docker images

To avoid problems it's recommended to push the images to a container registry. This can be easilly done locally with a Docker container:
	
	docker run -d -p 5000:5000 --restart=always --name registry registry:2

Tag and push the image:

	docker tag helloworld:1.0 localhost:5000/helloworld 
	docker push localhost:5000/helloworld

Now test if K3s can access the image crating a deployment:

	kubectl create deployment helloworld --image=localhost:5000/helloworld --port=8080 --replicas=2

	kubectl expose deployment/helloworld --type="NodePort" --port 8080

Check:

	curl localhost:NODE_PORT


