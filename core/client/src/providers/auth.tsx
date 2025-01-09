import { ReactNode, useState } from 'react';
import { Navigate, Outlet, useNavigate } from 'react-router-dom';
import secureLocalStorage from 'react-secure-storage';

import { AxiosError, AxiosResponse } from 'axios';

import { getCookie, removeCookie } from 'typescript-cookie';

import { Box } from '@mui/material';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';
import { ErrorData, ErrorHandler, handleErrors } from '@/api/errors';
import Navbar from '@/components/Navbar';
import { AuthContext, useAuth } from '@/hooks/auth';

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();

  const [token, setToken] = useState<string | undefined>(
    getCookie('access_token')
  );
  const [user, setUser] = useState<model.User | null>(
    secureLocalStorage.getItem('user') as model.User
  );

  const [{ loading }, request] = useAxios(
    {},
    {
      manual: true,
    }
  );

  const login = async (
    data: request.Authorization,
    errorHandler: ErrorHandler
  ) => {
    try {
      const response: AxiosResponse<response.Authorization> = await request({
        url: ENDPOINTS.authorization,
        method: 'POST',
        data,
      });
      setToken(response.data.access);
      secureLocalStorage.setItem('user', response.data.user);
      setUser(response.data.user);
    } catch (err) {
      const error = (err as AxiosError).response?.data as ErrorData;
      handleErrors(error.details, errorHandler);
    }
  };

  const register = async (
    data: request.Registration,
    errorHandler: ErrorHandler
  ) => {
    try {
      const response: AxiosResponse<response.Registration> = await request({
        url: ENDPOINTS.registration,
        method: 'POST',
        data,
      });
      const loginData = {
        email: response.data.email,
        password: data.password,
      };
      await login(loginData, errorHandler);
    } catch (err) {
      const error = (err as AxiosError).response?.data as ErrorData;
      handleErrors(error.details, errorHandler);
    }
  };

  const logout = () => {
    removeCookie('access_token');
    secureLocalStorage.removeItem('user');
    setToken(undefined);
    setUser(null);
    navigate('/sign-in', { replace: true });
  };

  const value = {
    loading,
    token,
    user,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const GuestRoutes = () => {
  const { token, user } = useAuth();
  return !token || !user ? <Outlet /> : <Navigate to="/" replace />;
};

export const AuthorizedRoutes = () => {
  const { token, user } = useAuth();
  return token && user ? (
    <Box>
      <Navbar />
      <Outlet />
    </Box>
  ) : (
    <Navigate to="/sign-in" replace />
  );
};

export default AuthProvider;
