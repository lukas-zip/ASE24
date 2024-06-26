import { request } from './request';

export const signIn = (data) => request("user", 'post', '/login', data);

// Users API
export const signUpForUser = (data) => request("user", 'post', '/users', data);
export const updateUser = (userId, data) => request("user", 'put', `/users/${userId}`, data);
export const getUserById = (userId) => request("user", 'get', `/users/${userId}`);
export const deleteUser = (userId) => request("user", 'delete', `/users/${userId}`);
export const postPictureForUserService_profile = (data) => request("user", 'post', `/picture/profile`, data);
export const postPictureForUserService_shoppictures = (data) => request("user", 'post', `/picture/shop`, data);

// Shops API
export const signUpForShop = (data) => request("user", 'post', '/shops', data);
export const updateShop = (shopId, data) => request("user", 'put', `/shops/${shopId}`, { ...data, action: "update" });
export const getShopById = (shopId) => request("user", 'get', `/shops/${shopId}`);
export const deleteShop = (shopId) => request("user", 'delete', `/shops/${shopId}`);

// Products API (Port 8002)
export const getAllProductsByShopId = (shopId) => request("products", 'get', `/product/cataloguesell/${shopId}`);
export const getProductById = (productId) => request("products", 'get', `/product/${productId}`);
export const searchProducts = (searchTerm) => request("products", 'get', `/product/search?term=${searchTerm}`);
export const deleteProductFromCompany = (productId) => request("products", 'delete', `/product/delete`, { product_id: productId });
export const updateProductForCompany = (productId, data) => request("products", 'put', `/product/update_product/${productId}`, data);
export const addProductForCompany = (data) => request("products", 'post', `/product/insert`, data);
export const uploadProductPicture = (data) => request("products", 'post', `/product/upload/picture`, data);

export const getProductByCategory = (category) => request("products", 'get', `/product/category?term=${category}`);

// Orders API
//user
export const getUserUnpaidOrders = (userID) => request("orders", 'get', `/orders/search/user/${userID}/status/unpaid`);
export const getUserPaidOrders = (userID) => request("orders", 'get', `/orders/search/user/${userID}/status/paid`);
//seller
export const getSellerPaidOrders = (sellerID) => request("orders", 'get', `/orders/search/po/${sellerID}/status/paid`);
export const getSellerUnpaidOrders = (sellerID) => request("orders", 'get', `/orders/search/po/${sellerID}/status/unpaid`);

export const removeProductFromOrder = (orderID, data) => request("orders", 'put', `/orders/${orderID}`, data);
export const addProductIntoOrder = (orderID, data) => request("orders", 'put', `/orders/${orderID}`, data);
export const getOrderByUserId = (userID) => request("orders", 'get', `/orders/users/search/${userID}`);
export const getOrderByShopId = (sellerID) => request("orders", 'get', `/orders/product/search/${sellerID}`);
export const deleteOrder = (orderId) => request("orders", 'delete', `/orders/${orderId}`);
export const updateOrder = (orderId, data) => request("orders", 'put', `/orders/${orderId}`, data);
export const createOrder = (data) => request("orders", 'post', '/orders', data);


// payment
export const createPaymentIntent = (data) => request("payment", 'post', '/create-payment-intent', data);
// {
//     "order_id": "fdefe9fe-1a9c-48be-b9ac-e13e98788e0c",
//     "total_price": 82.32,
//     "user_id": "384172b4-3aa6-490e-bda5-e90d0dfccfab"
// }


// Reviews API (Port 8003)
export const createReview = (data) => request("reviews", 'post', `/review`, data);
export const deleteReview = (data) => request("reviews", 'delete', `/review`, data);
export const getReviewByProductId = (productId) => request("reviews", 'get', `/review/${productId}`);
export const updateReview = (data) => request("reviews", 'put', `/review`, data);
export const getBatchReviews = () => request("reviews", 'get', '/review/getbatch');