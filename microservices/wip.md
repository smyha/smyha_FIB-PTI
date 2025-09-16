
#https://docs.k3s.io/quick-start


Execute the following command will create a single-node Kubernetes cluster:

	curl -sfL https://get.k3s.io | sh -

The command also installs kubectl and creates a kubeconfig file (/etc/rancher/k3s/k3s.yaml). 

To be able to run k3s commands without sudo do the following:


	mkdir -p .kube && sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config && sudo chown $USER ~/.kube/config && chmod 600 ~/.kube/config && export KUBECONFIG=~/.kube/config

Test:

	kubectl get node
	
Launch a Docker registry:	
	
	docker run -d -p 5000:5000 --restart=always --name registry registry:2

Tag and push the image:

	docker tag helloworld:1.0 localhost:5000/helloworld 
	docker push localhost:5000/helloworld

kubectl create deployment helloworld --image=localhost:5000/helloworld --port=8080 --replicas=2

	kubectl expose deployment/helloworld --type="NodePort" --port 8080

	curl localhost:NODE_PORT


----------------------------------------------------------
two-machines cluster

v1

SERVER NODE:

	curl -sfL https://get.k3s.io | sh -
	cat /var/lib/rancher/k3s/server/node-token

SECONDARY NODE:

	curl -sfL https://get.k3s.io | K3S_URL=https://myserver:6443 K3S_TOKEN=mynodetoken sh -
	
	NOTE: Each machine must have a unique hostname. If your machines do not have unique hostnames, pass the K3S_NODE_NAME environment variable and provide a value with a valid and unique hostname for each node.


v2

SERVER NODE:

	wget https://github.com/k3s-io/k3s/releases/download/v1.23.5%2Bk3s1/k3s
	chmod +x k3s
	sudo ./k3s server
	
	sudo ./k3s kubectl get nodes
	
	cat /var/lib/rancher/k3s/server/node-token
	
	NODE-TOKEN
	
SECONDARY NODE:

	sudo ./k3s agent --server https://myserver:6443 --token NODE-TOKEN

	
----------------------------------------------------------
KUBECTL

https://kubernetes.io/docs/reference/kubectl/

kubectl config set-context --current --namespace=<namespace-name>
