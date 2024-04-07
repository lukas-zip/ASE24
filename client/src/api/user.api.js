import { request } from './request';

export const signIn = (data) => request("user", 'post', '/login', data);

// Users API
export const signUpForUser = (data) => request("user", 'post', '/users', data);
export const updateUser = (userId, data) => request("user", 'put', `/users/${userId}`, data);
export const getUserById = (userId) => request("user", 'get', `/users/${userId}`);
export const deleteUser = (userId) => request("user", 'delete', `/users/${userId}`);

// Shops API
export const signUpForShop = (data) => request("user", 'post', '/shops', data);
export const updateShop = (shopId, data) => request("user", 'put', `/shops/${shopId}`, data);
export const getShopById = (shopId) => request("user", 'get', `/shops/${shopId}`);
export const deleteShop = (shopId) => request("user", 'delete', `/shops/${shopId}`);

// Products API (Port 8002)
export const getAllProductsByShopId = (shopId) => request("products", 'get', `/product/cataloguesell/${shopId}`);
export const getProductById = (productId) => request("products", 'get', `/products/${productId}`);
export const searchProducts = (data) => request("products", 'post', '/products/search', data);
export const deleteProductFromCompany = (productId) => request("products", 'delete', `/products/delete`, { product_id: productId });
export const updateProductForCompany = (productId, data) => request("products", 'put', `/products//product/update_product/${productId}`, data);
export const addProductForCompany = (productId, companyId, data) => request("products", 'post', `/product/insert`, data);
// Orders API
export const getOrderById = (orderId) => request("orders", 'get', `/orders/${orderId}`);
export const deleteOrder = (orderId) => request("orders", 'delete', `/orders/${orderId}`);
export const updateOrder = (orderId, data) => request("orders", 'put', `/orders/${orderId}`, data);
export const createOrder = (data) => request("orders", 'post', '/orders', data);

// Reviews API (Port 8003)
export const createReview = (data) => request("reviews", 'post', `/review`, data);
export const deleteReview = (reviewId) => request("reviews", 'delete', `/review/${reviewId}`);
export const getReviewByProductId = (productId) => request("reviews", 'get', `/review/${productId}`);
export const updateReview = (reviewId, data) => request("reviews", 'put', `/review/${reviewId}`, data);
export const getBatchReviews = () => request("reviews", 'get', '/review/getbatch');