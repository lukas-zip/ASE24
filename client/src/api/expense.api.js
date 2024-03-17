import { request } from "./request";

export const getExpenseByUserId = (id) =>
  request("get", `/expense/get-by-user/${id}`);

export const getAllExpensesByMonth = (userId, params) =>
  request("get", `/expense/get-monthly-by-user/${userId}`, params);

export const getAllExpensesByDay = (userId, params) =>
  request("get", `/expense/get-expense-by-date/${userId}`, params);

export const createExpense = (params) =>
  request("post", "/expense/create-expense", params);

export const updateExpense = (params) =>
  request("put", `/expense/update-expense/${params.expense_id}`, params);

export const deleteExpense = (id) =>
  request("delete", `/expense/delete-expense/${id}`);
