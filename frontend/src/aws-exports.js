const awsmobile = {
  Auth: {
    region: process.env.VUE_APP_AWS_REGION,
    userPoolId: process.env.VUE_APP_USER_POOL_ID,
    userPoolWebClientId: process.env.VUE_APP_USER_POOL_CLIENT_ID
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