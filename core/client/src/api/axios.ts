import secureLocalStorage from 'react-secure-storage';

import axios, {
  AxiosError,
  AxiosResponse,
  HttpStatusCode,
  InternalAxiosRequestConfig,
} from 'axios';
import { makeUseAxios } from 'axios-hooks';

import { getCookie, removeCookie } from 'typescript-cookie';

const instance = axios.create({
  baseURL:
    import.meta.env.MODE === 'development' ? import.meta.env.VITE_API_URL : '',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'multipart/form-data',
  },
  withCredentials: true,
});

instance.interceptors.request.use(
  async (request: InternalAxiosRequestConfig) => {
    const csrf = getCookie('csrftoken');
    if (csrf !== undefined) {
      request.headers['X-CSRFToken'] = csrf;
    }
    const token = getCookie('access_token');
    if (token) {
      request.headers.Authorization = `Bearer ${token}`;
    }
    return request;
  },
  async (error: AxiosError) => Promise.reject(error)
);
instance.interceptors.response.use(
  async (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    if (
      getCookie('access_token') &&
      secureLocalStorage.getItem('user') &&
      (error.response?.status === HttpStatusCode.Unauthorized ||
        error.response?.status === HttpStatusCode.Forbidden)
    ) {
      removeCookie('access_token');
      secureLocalStorage.removeItem('user');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

export const useAxios = makeUseAxios({
  axios: instance,
});
