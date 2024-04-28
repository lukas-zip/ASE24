import { message as $message } from 'antd';
import axios from 'axios';
import { store } from '@/store';
import { setGlobalState } from '@/store/global.store';

const serviceBases = {
    user: 'http://127.0.0.1:8001', // 默认服务端口
    products: 'http://127.0.0.1:8002', // 产品服务端口
    reviews: 'http://127.0.0.1:8003', // 评论服务端口
    orders: 'http://127.0.0.1:8004', // 订单服务端口
    payment: 'http://127.0.0.1:8005', // 支付服务端口
    // 其他服务端口...
};

const createAxiosInstance = (baseURL) => axios.create({ baseURL });


export const request = (serviceType, method, url, data, config) => {
    const axiosInstance = createAxiosInstance(serviceBases[serviceType]);
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
            // $message.error(error?.response?.data ? error.response.data : errorMessage)
            return {
                status: false,
                message: error?.response?.data ? error.response.data : errorMessage,
                result: null,
            };
        },
    );
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
            return axiosInstance.delete(url, { data: data, ...configWithParams });
        case 'put':
            return axiosInstance.put(url, data, configWithParams);
        default:
            break;
    }
};