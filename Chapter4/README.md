# Command line work with EKS

## Step-01: Create EKS Cluster using eksctl
- It will take 15 to 20 minutes to create the Cluster Control Plane 
```sh
# Create Cluster
eksctl create cluster --name=eksdemo1 \
                      --region=us-east-1 \
                      --zones=us-east-1a,us-east-1b,us-east-1c \
                      --without-nodegroup 


# Get List of clusters
eksctl get cluster 

```
## Step-02: Create & Associate IAM OIDC Provider for our EKS Cluster
- To enable and use AWS IAM roles for Kubernetes service accounts on our EKS cluster, we must create &  associate OIDC identity provider.
``` sh                 

# Replace with region & cluster name
eksctl utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster eksdemo1 \
    --approve

```

## Step-03: Create EC2 Keypair
- Create a new EC2 Keypair with name as `Instance-key`


## Step-04: Create Node Group with additional Add-Ons in Public Subnets
- These add-ons will create the respective IAM policies for us automatically within our Node Group role.
 ```sh
# Create Public Node Group   
eksctl create nodegroup --cluster=eksdemo1 \
                        --region=us-east-1 \
                        --name=eksdemo1-ng-public1 \
                        --node-type=t2.medium \
                        --nodes=2 \
                        --nodes-min=2 \
                        --nodes-max=4 \
                        --node-volume-size=20 \
                        --ssh-access \
                        --ssh-public-key=kube-demo \
                        --managed \
                        --asg-access \
                        --external-dns-access \
                        --full-ecr-access \
                        --appmesh-access \
                        --alb-ingress-access


```

### Note : If kubectl can't get information
### Configure kubeconfig for kubectl
```sh
eksctl get cluster # TO GET CLUSTER NAME

aws eks --region us-east-1 update-kubeconfig --name eksdemo1

export AWS_ACCESS_KEY_ID={your-aws-access-key}
export AWS_SECRET_ACCESS_KEY={your-aws-secret-access-key}

```
## Step-05: Create IAM Policy
```sh
# Download IAM Policy
## Download latest
curl -o iam_policy_latest.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json


aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy_latest.json




```
## Step-06: Create IAM Role using eksctl
```sh
# Replaced name, cluster and policy arn (Policy arn we took note in step-02)
eksctl create iamserviceaccount \
  --cluster=eksdemo1 \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::736059458620:policy/AWSLoadBalancerControllerIAMPolicy \
  --override-existing-serviceaccounts \
  --approve


# Get IAM Service Account
eksctl  get iamserviceaccount --cluster eksdemo1
```  
### Step-07: Install AWS Load Balancer Controller
```sh
# Add the eks-charts repository.
helm repo add eks https://aws.github.io/eks-charts

# Update your local repo to make sure that you have the most recent charts.
helm repo update

# Install the AWS Load Balancer Controller.

## --set vpcId=vpc-xxxxxxxx
## Replace Cluster Name, Region Code, VPC ID, Image Repo Account ID and Region Code  
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=eksdemo1 \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=us-east-1 \
  --set vpcId=vpc-06fef6ee4d3ae40af \
  --set image.repository=602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon/aws-load-balancer-controller



# List Pods
kubectl get pods -n kube-system
```  


### Delete eks cluster and nodegroup

```sh

# Uninstall AWS Load Balancer Controller
helm uninstall aws-load-balancer-controller -n kube-system

# Delete Node Group
eksctl delete nodegroup --cluster=eksdemo1 --name=eksdemo1-ng-public1


# Delete Cluster
eksctl delete cluster eksdemo1

```