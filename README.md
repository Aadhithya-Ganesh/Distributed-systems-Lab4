### Distributed systems LAB 4

The purpose of this lab is to design and implement a simple application comprised of at least two distinct microservices that interact with each other. The application should have:

1. Well-defined service boundaries
2. Inter-service communication
3. Deployment of microservices

---

### Prerequisites

Ensure you have Minikube and kubectl installed before proceeding. You can download it here:

[Minikube install guide](https://kubernetes.io/docs/tutorials/hello-minikube/)<br/>
[Kubectl install guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)

---

### Running the application

1. **Start minikube cluster**
   ```bash
   minikube start
   ```
1. **Go into the kubernetes folder**
   ```bash
   cd kubernetes
   ```
2. **In the root directory, start deployments and services**
   ```bash
   kubectl apply -f booking-service-deployments.yaml -f booking-service-services.yaml -f database-deployments.yaml -f database-service.yaml -f frontend-deployments.yaml -f frontend-services.yaml -f item-service-deployments.yaml -f item-service-services.yaml
   ```
3. **Expose the items service**
   ```bash
   kubectl port-forward svc/item-service 8080:8080
   ```
 
4. **Adding 1 record to the items DB. Note: You cannot directly copy and paste this command to Windows command prompt. Use git-bash or postman to execute the command**
   ```bash
   curl --location 'localhost:8080/items' --header 'Content-Type: application/json' --data '{
    "name": "bottle",
    "description": "You can drink",
    "price": "5",
    "quantity": 20
   }'
   ```
1. **For checking the output, run the below command and visit localhost:80**
   ```bash
   kubectl port-forward svc/frontend 80:80
   ```

---

### Frontend endpoints

Your client service is exposed at:
http://localhost:80
(after running: kubectl port-forward svc/web-app-service 80:80)
