import { request } from './request';

export const createNewBudget = (params) => request('post', '/budget/create', null, { params });
// format {
// startDate  dd-MM-yyyy
// endDate
// name
// budgetAmount
// comments
//  userId
// }

export const deleteBudget = (params) => request('delete', '/budget/delete', params);
// format {
//  budgetId: xx
// }
export const updateBudget = (params) => request('put', `/budget/update`, null, { params });

// format {
//     budgetId
// name
// startDate: dd-MM-yyyy
// endDate: dd-MM-yyyy
// comments
// budgetAmount
// }

export const getBudgetByID = (id) => request('get', `/budget/${id}`);
export const getCurrentBudget = (id) => request('get', `/budget/getCurrentBudget/${id}`);
export const getBudgetByUserID = (id) => request('get', `/budget/getByUserId/${id}`);

export const getBalanceMonthly = (data, params) => request('get', `/budget/monthly-balance`, data, { params });
export const getBalanceYearly = (data, params) => request('get', `/budget/yearly-balance`, data, { params });
export const getBalanceDaily = (data, params) => request('get', `/budget/daily-balance`, data, { params });
// format {userId:x}

export const getBalanceOverview = (userId) => request('get', `/budget/getBalanceOverview/${userId}`);