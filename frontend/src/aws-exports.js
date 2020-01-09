const awsmobile = {
  Auth: {
    region: process.env.VUE_AWS_REGION,
    userPoolId: process.env.VUE_APP_AWS_COGNITO_USER_POOL_ID,
    userPoolWebClientId: process.env.VUE_APP_AWS_COGNITO_CLIENT_ID,
    cookieStorage: {
      domain: 'localhost',
      secure: false,
      path: '/',
      expires: 1
    }
  },
  API: {
    endpoints: [{
        name: "CartAPI",
        endpoint: process.env.VUE_APP_CART_API_URL
      },
      {
        name: "ProductAPI",
        endpoint: process.env.VUE_APP_PRODUCTS_API_URL,

      }
    ]
  }
};

export default awsmobile;