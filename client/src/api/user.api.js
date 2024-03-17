import { request } from './request';

export const signUp = (data) => request('post', '/user/create', data);

export const signIn = (data) => request('post', '/user/login', data);

export const updatePassword = (userID, data) => request('put', `/user/update-password/${userID}/`, data);




