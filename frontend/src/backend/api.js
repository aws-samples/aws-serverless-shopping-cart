import { Auth, API } from "aws-amplify";

async function getHeaders() {
  const headers = {
    "Content-Type": "application/json",
  };

  let session = null;
  try {
    session = await Auth.currentSession();
  } catch (e) {
    console.error("Error getting current session:", e);
  }

  if (session) {
    let authHeader = session.getIdToken().jwtToken;
    headers["Authorization"] = authHeader;
  }
  return headers;
}

export async function getCart() {
  return getHeaders().then((headers) =>
    API.get("CartAPI", "/cart", {
      headers: headers,
      withCredentials: true,
    })
  );
}

export async function postCart(obj, quantity = 1) {
  return getHeaders().then((headers) =>
    API.post("CartAPI", "/cart", {
      body: {
        productId: obj.productId,
        quantity: quantity,
      },
      headers: headers,
      withCredentials: true,
    })
  );
}

export async function putCart(obj, quantity) {
  return getHeaders().then((headers) =>
    API.put("CartAPI", "/cart/" + obj.productId, {
      body: {
        productId: obj.productId,
        quantity: quantity,
      },
      headers: headers,
      withCredentials: true,
    })
  );
}

export async function getProducts() {
  return getHeaders().then((headers) =>
    API.get("ProductAPI", "/product", {
      headers: headers,
      withCredentials: true,
    })
  );
}

export async function getDiscountedProducts() {
  return getHeaders().then((headers) =>
    API.get("DiscountedProductAPI", "/discounted_product", {
      headers: headers,
    })
  );
}

export async function cartMigrate() {
  return getHeaders().then((headers) =>
    API.post("CartAPI", "/cart/migrate", {
      headers: headers,
      withCredentials: true,
    })
  );
}

export async function cartCheckout() {
  return getHeaders().then((headers) =>
    API.post("CartAPI", "/cart/checkout", {
      headers: headers,
      withCredentials: true,
    })
  );
}
