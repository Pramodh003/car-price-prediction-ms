Microservice Architecture

![image](https://github.com/user-attachments/assets/ca8f0ca8-cac1-466c-a298-7e65ce2a3879)

#### I have created simple machine learning models which is used to predict the car price.
#### In this there are 2 microservice and one job
##### 1.Gateway
##### 2.Auth
##### 3.Predict

#### In Gateway it will route the login request to auth microservice and we also upload the data to database and this data id is sent to rabbitq and this consumer job take this Id , fetch the respective data using that id and then give prediction also update the predicted price in database

#### Terraform script is used for creating eks cluster & nodes in private subnets which also includes setting up loadbalancer & Letsecrypt for ssl.

#### Used kubernetes manifest for deployment different microservice. It also includes pub/sub arch and for that I have used keda jobs for scaling  & for microservices I have used HPA for scaling jobs

#### Created a Reusable github actions for CI/CD 
