export const debounce = (func: (arg0: any) => any | void, wait: number | undefined) => {
    let timeout: string | number | NodeJS.Timeout | undefined;
    // @ts-ignore
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            // @ts-ignore
            func(...args);
        };

        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};