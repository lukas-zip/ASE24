function myDebounceFunc(fn, delay) {
    let timeout;
    return function () {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            fn.apply(this, arguments)
        }, delay)
    }
}

export { myDebounceFunc }