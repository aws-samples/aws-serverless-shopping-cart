process.env.AWS_SDK_LOAD_CONFIG = true;
var fs = require('fs');

var args = process.argv.slice(2);
var envtype = args[0] ? args[0] : 'local'
var AWS = require('aws-sdk');
var ssm = new AWS.SSM();


const query = {
    "Path": "/serverless-shopping-cart-demo/",
    "WithDecryption": false,
    "Recursive": true
}

const requiredParams = ["CART_API_URL", "PRODUCTS_API_URL", "USER_POOL_ID",
    "USER_POOL_CLIENT_ID"
]

var params = ssm.getParametersByPath(query).promise()

var output = []

function formatParams(data) {
    for (var param of data) {
        const paramName = param.Name.toUpperCase().split("/").pop().replace(/-/g, "_")
        if (requiredParams.includes(paramName)) {
            output.push("VUE_APP_" + paramName + '=' + param.Value)
        }
    }
}

params
    .then(data => {
        formatParams(data.Parameters)
        output.push("VUE_APP_AWS_REGION=" + AWS.config.region)
        var fileName = "./.env." + envtype
        fs.writeFile(fileName, output.join('\n'), function (err) {
            if (err) {
                return console.log(err);
            }
            console.log(`env file ${fileName} populated with config`);
        });

    })
    .catch(error => {
        console.log('error: ' + error)
    })


/*
VUE_APP_CART_API_URL=CartApiUrl
VUE_APP_PRODUCTS_API_URL=ProductApiUrl
VUE_APP_AWS_REGION=your-aws-region
VUE_APP_AWS_COGNITO_USER_POOL_ID=CognitoUserPoolId
VUE_APP_AWS_COGNITO_CLIENT_ID=CognitoAppClientId
*/