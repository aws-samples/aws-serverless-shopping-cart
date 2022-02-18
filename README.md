# Serverless Shopping Cart Microservice

This application is a sample application to demonstrate how you could implement a shopping cart microservice using 
serverless technologies on AWS. The backend is built as a REST API interface, making use of [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [AWS Lambda](https://aws.amazon.com/lambda/), [Amazon Cognito](https://aws.amazon.com/cognito/), and [Amazon DynamoDB](https://aws.amazon.com/dynamodb/). The frontend is a Vue.js application using the [AWS Amplify](https://aws-amplify.github.io/) SDK for authentication and communication with the API.

To assist in demonstrating the functionality, a bare bones mock "products" service has also been included. Since the 
authentication parts are likely to be shared between components, there is a separate template for it. The front-end 
doesn't make any real payment integration at this time.

## Architecture & Design

![Architecture Diagram](./images/architecture.png)

## Design Notes

Before building the application, I set some requirements on how the cart should behave:

- Users should be able to add items to the cart without logging in (an "anonymous cart"), and that cart should persist 
across browser restarts etc.
- When logging in, if there were products in an anonymous cart, they should be added to the user's cart from any 
previous logged in sessions.
- When logging out, the anonymous cart should not have products in it any longer.
- Items in an anonymous cart should be removed after a period of time, and items in a logged in cart should persist 
for a longer period.
- Admin users to be able to get an aggregated view of the total number of each product in users' carts at any time.

### Cart Migration

When an item is added to the cart, an item is written in DynamoDB with an identifier which matches a randomly generated 
(uuid) cookie which is set in the browser. This allows a user to add items to cart and come back to the page later 
without losing the items they have added. When the user logs in, these items will be removed, and replaced with items 
with a user id as the pk. If the user already had that product in their cart from a previous logged in session, the 
quantities would be summed. Because we don't need the deletion of old items to happen immediately as part of a 
synchronous workflow, we put messages onto an SQS queue, which triggers a worker function to delete the messages.  

To expire items from users' shopping carts, DynamoDB's native functionality is used where a TTL is written along with 
the item, after which the item should be removed. In this implementation, the TTL defaults to 1 day for anonymous 
carts, and 7 days for logged in carts.  

### Aggregated View of Products in Carts

It would be possible to scan our entire DynamoDB table and sum up the quantities of all the products, but this will be 
expensive past a certain scale. Instead, we can calculate the total as a running process, and keep track of the total 
amount.  

When an item is added, deleted or updated in DynamoDB, an event is put onto DynamoDB Streams, which in turn triggers a 
Lambda function. This function calculates the change in total quantity for each product in users' carts, and writes the 
quantity back to DynamoDB. The Lambda function is configured so that it will run after either 60 seconds pass, or 100 
new events are on the stream. This would enable an admin user to get real time data about the popular products, which 
could in turn help anticipate inventory. In this implementation, the API is exposed without authentication to 
demonstrate the functionality.  


## Api Design

### Shopping Cart Service

GET  
`/cart`  
Retrieves the shopping cart for a user who is either anonymous or logged in.  

POST  
`/cart`  
Accepts a product id and quantity as json. Adds specified quantity of an item to cart.  

`/cart/migrate`  
Called after logging in - migrates items in an anonymous user's cart to belong to their logged in user. If you already 
have a cart on your logged in user, your "anonymous cart" will be merged with it when you log in.

`/cart/checkout`  
Currently just empties cart.

PUT  
`/cart/{product-id}`  
Accepts a product id and quantity as json. Updates quantity of given item to provided quantity.  

GET  
`/cart/{product-id}/total`  
Returns the total amount of a given product across all carts. This API is not used by the frontend but can be manually 
called to test.  

### Product Mock Service

GET  
`/product`  
Returns details for all products.  

`/product/{product_id}`  
Returns details for a single product.  

## Running the Example

### Requirements

python >= 3.8.0
boto3
SAM CLI, >= version 0.50.0  
AWS CLI  
yarn  

### Setup steps

Fork the github repo, then clone your fork locally: 
`git clone https://github.com/<your-github-username>/aws-serverless-shopping-cart && cd aws-serverless-shopping-cart`

If you wish to use a named profile for your AWS credentials, you can set the environment variable `AWS_PROFILE` before 
running the below commands. For a profile named "development": `export AWS_PROFILE=development`.  

You now have 2 options - you can deploy the backend and run the frontend locally, or you can deploy the whole project 
using the AWS Amplify console.

## Option 1 - Deploy backend and run frontend locally
### Deploy the Backend

An S3 bucket will be automatically created for you which will be used for deploying source code to AWS. If you wish to 
use an existing bucket instead, you can manually set the `S3_BUCKET` environment variable to the name of your bucket.  

Build and deploy the resources:  
``` bash
make backend  # Creates S3 bucket if not existing already, then deploys CloudFormation stacks for authentication, a 
product mock service and the shopping cart service.  
```

### Run the Frontend Locally

Start the frontend locally:  
``` bash
make frontend-serve  # Retrieves backend config from ssm parameter store to a .env file, then starts service.  
```

Once the service is running, you can access the frontend on http://localhost:8080/ and start adding items to your cart. 
You can create an account by clicking on "Sign In" then "Create Account". Be sure to use a valid email address as 
you'll need to retrieve the verification code.

**Note:** CORS headers on the backend service default to allowing http://localhost:8080/. You will see CORS errors if 
you access the frontend using the ip (http://127.0.0.1:8080/), or using a port other than 8080.  

### Clean Up
Delete the CloudFormation stacks created by this project:
``` bash
make backend-delete
```

## Option 2 - Automatically deploy backend and frontend using Amplify Console


[![One-click deployment](https://oneclick.amplifyapp.com/button.svg)](https://console.aws.amazon.com/amplify/home#/deploy?repo=https://github.com/aws-samples/aws-serverless-shopping-cart)

1) Use **1-click deployment** button above, and continue by clicking "Connect to Github"
2) If you don't have an IAM Service Role with admin permissions, select "Create new role". Otherwise proceed to step 5) 
3) Select "Amplify" from the drop-down, and select "Amplify - Backend Deployment", then click "Next".
4) Click "Next" again, then give the role a name and click "Create role"
5) In the Amplify console and select the role you created, then click "Save and deploy"
6) Amplify Console will fork this repository into your GitHub account and deploy it for you
7) You should now be able to see your app being deployed in the [Amplify Console](https://console.aws.amazon.com/amplify/home)
8) Within your new app in Amplify Console, wait for deployment to complete (this should take approximately 12 minutes for the first deploy)


### Clean Up
Delete the CloudFormation stacks created by this project. There are 3 of them, with names starting with "aws-serverless-shopping-cart-".

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.  
