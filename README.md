# Serverless Shopping Cart Microservice

This application is a sample application to demonstrate how you could implement a shopping cart microservice using serverless technologies on AWS. The backend is built with a REST API interface, making use of [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [AWS Lambda](https://aws.amazon.com/lambda/), [Amazon Cognito](https://aws.amazon.com/cognito/), and [Amazon DynamoDB](https://aws.amazon.com/dynamodb/). The frontend is a Vue.js application using the [AWS Amplify](https://aws-amplify.github.io/) SDK.

To assist in demonstrating the functionality, a bare bones mock "products" service has also been included. Since the authentication parts are likely to be shared between components, there is a separate template for it. The front-end doesn't make any real payment integration at this time.

## Architecture

![Architecture Diagram](./architecture.png)

## Api Design

### Shopping Cart Service

GET  
`/cart`  

POST  
`/cart`  
`/cart/migrate`  
`/cart/checkout`  

PUT  
`/cart/{product-id}`  

### Product Mock Service

GET  
`/product`  
`/product/{product_id}`  

## Running the Example

### Requirements

python >= 3.8.0
SAM CLI, >= version 0.33.1  
AWS CLI  
AWS Account  

### Deploy the Backend

Clone the project: `git clone <repo-url> && cd <repo-dir>`

Build and deploy the resources, making note of the output variables:
``` bash
cd backend
export S3_BUCKET=your-s3-bucket-name
make TEMPLATE=auth  # Deploys the authentication infrastructure. Make a note of the outputs "CognitoUserPoolId" and "CognitoAppClientId".
make TEMPLATE=product-mock  # Deploys the product mock service. Make a note of the output url "ProductApi".
make build_layers  # Locally builds python lambda layers required for deploying shoppingcart-service
make TEMPLATE=shoppingcart-service  # Deploys the SAM template for the shopping-cart service. Make a note of the output url "CartApi". 

```

Create a user you can use to log in with. Replace CognitoUserPoolId with the value you noted down in previous step. 
Feel free to change the username or temporary password (this will be used for the first login before prompting you to change it):  
```bash
aws cognito-idp admin-create-user --username testuser1 --temporary-password Testuser1! --user-pool-id CognitoUserPoolId 
```

### Run the Frontend Locally

Create a file `.env.local` inside the `frontend` directory with the following content, using the values you took a note 
of in the previous step, as well as the aws region you will deploy to (for example eu-west-1):  
``` js
VUE_APP_CART_API_URL=CartApiUrl
VUE_APP_PRODUCTS_API_URL=ProductApiUrl
VUE_APP_AWS_REGION=your-aws-region
VUE_APP_AWS_COGNITO_USER_POOL_ID=CognitoUserPoolId
VUE_APP_AWS_COGNITO_CLIENT_ID=CognitoAppClientId
```

Start the frontend locally:  
``` bash
cd frontend
yarn install
yarn serve
```
Access on http://localhost:8080/ (not http://127.0.0.1:8080/) in your browser. Using a different port, or using the 
ip address will cause errors due to the backend's CORS configuration.

## SAM Template Resources

### `shoppingcart-service.yaml`
AWS Lambda  
AWS IAM  
Amazon API Gateway  
Amazon DynamoDB  
AWS Systems Manager  

### `auth.yaml`
Cognito User Pool  
Cognito User Pool Client  
AWS Systems Manager Parameter Store Parameter  

### `product-mock-service.yaml`
AWS Lambda  
Amazon API Gateway  

## Clean Up
Delete the CloudFormation stacks created by this project:
``` bash
make delete TEMPLATE=shoppingcart-service
make delete TEMPLATE=product-mock
make delete TEMPLATE=auth
```

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.  
