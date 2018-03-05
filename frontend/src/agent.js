/**
 * Created by jasonjohns on 6/6/17.
 */

import superagentPromise from 'superagent-promise';
import _superagent from 'superagent';
import {API_ROOT} from './config';

const superagent = superagentPromise(_superagent, global.Promise);
const responseBody = res => res.body;
const MAPBOX_API_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

if (!MAPBOX_API_TOKEN)
    throw new Error('Mapbox API token not set');

const requests = {
    get: url => superagent.get(url).then(responseBody),
};

const Tuition = {
    get: () => requests.get(`${API_ROOT}/tuition`),
};

const Institution = {
    get: (page = 1, full = false) => requests.get(`${API_ROOT}/institution?page=${page}&full=${full}`),
    getAllGeo: () => requests.get(`${API_ROOT}/institution?geo=true`),
    detail: (unitid) => requests.get(`${API_ROOT}/institution/${unitid}`),
    completions: (unitid) => requests.get(`${API_ROOT}/institution/${unitid}/completions`),
    tuition: (unitid) => requests.get(`${API_ROOT}/institution/${unitid}/tuition`),
    search: (term, page = 1, full = false) => requests.get(`${API_ROOT}/institution?page=${page}&full=${full}&search=${term}`)
};

export {
    Institution,
    Tuition,
    MAPBOX_API_TOKEN
}