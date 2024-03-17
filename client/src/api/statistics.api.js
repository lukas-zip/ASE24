import { request } from "./request";

export const getOverallSummary = (userId, params) =>
  request("get", `/statistics/get-overall-summary/${userId}`, params);

export const getMonthlySummary = (userId, params) =>
  request("get", `/statistics/get-monthly-summary/${userId}`, params);

export const getCategorySummary = (userId, params) =>
  request("get", `/statistics/get-category-summary/${userId}`, params);

export const getCategorySummaryByDay = (userId, params) =>
  request("get", `/statistics/get-category-summary-by-day/${userId}`, params);

export const getCategorySummaryByMonth = (userId, params) =>
  request("get", `/statistics/get-category-summary-by-month/${userId}`, params);

export const getExpensesByMonth = (userId, params) =>
  request("get", `/statistics/get-expenses-by-month/${userId}`, params);
