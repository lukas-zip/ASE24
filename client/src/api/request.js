import { message as $message } from 'antd';
import axios from 'axios';
import { store } from '@/store';
import { setGlobalState } from '@/store/global.store';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8082',
    // baseURL: 'https://medal.onrender.com/api',
    // timeout: 6000,
});

axiosInstance.interceptors.request.use(
    config => {
        store.dispatch(
            setGlobalState({
                loading: true,
            }),
        );
        return config;
    },
    error => {
        store.dispatch(
            setGlobalState({
                loading: false,
            }),
        );
        Promise.reject(error);
    },
);

axiosInstance.interceptors.response.use(
    config => {
        store.dispatch(
            setGlobalState({
                loading: false,
            }),
        );
        return config?.data;
    },
    error => {
        store.dispatch(
            setGlobalState({
                loading: false,
            }),
        );
        let errorMessage = 'error';

        if (error?.message?.includes('Network Error')) {
            errorMessage = 'network connection error!';
        } else {
            errorMessage = error?.message;
        }
        $message.error(error?.response?.data ? error.response.data : errorMessage)
        return {
            status: false,
            message: error?.response?.data ? error.response.data : errorMessage,
            result: null,
        };
    },
);

export const request = (method, url, data, config) => {
    const configWithParams = config ? {
        ...config,
        params: config.params, // 传递查询字符串参数
    } : {};

    switch (method) {
        case 'post':
            return axiosInstance.post(url, data, configWithParams);
        case 'get':
            return axiosInstance.get(url, { params: data, ...configWithParams });
        case 'delete':
            return axiosInstance.delete(url, { params: data, ...configWithParams });
        case 'put':
            return axiosInstance.put(url, data, configWithParams);
        default:
            break;
    }
};