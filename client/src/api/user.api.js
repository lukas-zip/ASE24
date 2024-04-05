import { request } from './request';

// Users API
const signInConfig = { action: "login" }
const signUpConfig = { action: "register" }
export const signIn = (data) => request("user", 'post', '/users', { ...signInConfig, ...data });
export const signUp = (data) => request("user", 'post', '/users', { ...signUpConfig, ...data });

export const updateUser = (userId, data) => request("user", 'put', `/users/${userId}`, data);

export const getUserById = (userId) => request("user", 'get', `/users/${userId}`);

export const deleteUser = (userId) => request("user", 'delete', `/users/${userId}`);

// Shops API
export const createShop = (data) => request("user", 'post', '/shops', data);

export const updateShop = (shopId, data) => request("user", 'put', `/shops/${shopId}`, data);

export const getShopById = (shopId) => request("user", 'get', `/shops/${shopId}`);

export const deleteShop = (shopId) => request("user", 'delete', `/shops/${shopId}`);

// Products API (Port 8002)
export const getProductById = (productId) => request("products", 'get', `/products/${productId}`);

export const searchProducts = (data) => request("products", 'post', '/products/search', data);

export const deleteProductFromCompany = (productId, companyId) => request("products", 'delete', `/products/${productId}/company/${companyId}`);

export const updateProductForCompany = (productId, companyId, data) => request("products", 'put', `/products/${productId}/company/${companyId}`, data);

export const addProductForCompany = (productId, companyId, data) => request("products", 'post', `/products/${productId}/company/${companyId}`, data);

// Orders API
export const getOrderById = (orderId) => request("orders", 'get', `/orders/${orderId}`);

export const deleteOrder = (orderId) => request("orders", 'delete', `/orders/${orderId}`);

export const updateOrder = (orderId, data) => request("orders", 'put', `/orders/${orderId}`, data);

export const createOrder = (data) => request("orders", 'post', '/orders', data);

// Reviews API (Port 8003)
export const createReview = (reviewId, data) => request("reviews", 'post', `/reviews/${reviewId}`, data);

export const deleteReview = (reviewId) => request("reviews", 'delete', `/reviews/${reviewId}`);

export const getReviewById = (reviewId) => request("reviews", 'get', `/reviews/${reviewId}`);

export const updateReview = (reviewId, data) => request("reviews", 'put', `/reviews/${reviewId}`, data);

export const getBatchReviews = () => request("reviews", 'get', '/review/getbatch');