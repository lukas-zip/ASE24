export const formatNumber = (num) => {
    if (Number.isInteger(num)) {
        return num.toString();  // 如果是整数，直接转换为字符串
    } else {
        // 如果是小数，转换为字符串并保留两位小数
        return num.toFixed(2);
    }
};