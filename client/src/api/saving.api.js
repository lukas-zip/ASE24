import { request } from './request';

export const createNewSaving = (data) => request('post', '/savings/create-saving', data);
export const updateSaving = (data, saving_id) => request('put', `/savings/update-saving/${saving_id}`, data);
// data format
// {
// user_id: user_id
// category_id: category_id
// targetDate: targetDate
// goal_val: goal_val
// saving_val: saving_val
// comments: comments
// }

// /add-more-saving/{saving_id}
export const addMoreSaving = (data, saving_id) => request('put', `/savings/add-more-saving/${saving_id}`, data);
// format
// { saving_val: saving_val }

// /delete-saving/{saving_id}
export const deleteSaving = (saving_id) => request('delete', `/savings/delete-saving/${saving_id}`);

// /{saving_id}
export const getSavingByID = (saving_id) => request('get', `/savings/${saving_id}`);

// /get-by-user/{user_id}
export const getSavingByUserID = (user_id) => request('get', `/savings/get-by-user/${user_id}`);

//get-all_expense-category
export const getExpenseCategories = (user_id) =>
  request("get", `/expense-category/get-all-expense-category/${user_id}/`);
  
//get-total-saving-by-category/{user_id}
export const getSavingTotalByCategories = (user_id) => request('get', `/savings/get-total-saving-by-category/${user_id}`);

