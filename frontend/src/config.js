/**
 * Created by jasonjohns on 6/6/17.
 */

const API_ROOT = (() => {
    const urlPath = 'api';
    
    if (process.env.NODE_ENV === 'development')
        return `http://192.168.33.10:8082/${urlPath}`;
})();

export {
    API_ROOT
}