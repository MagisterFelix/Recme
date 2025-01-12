import { ReactNode, useState } from 'react';
import { Navigate, Outlet, useNavigate } from 'react-router-dom';
import secureLocalStorage from 'react-secure-storage';

import { AxiosError, AxiosResponse } from 'axios';

import { removeCookie } from 'typescript-cookie';

import { Box } from '@mui/material';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';
import { ErrorData, ErrorHandler, handleErrors } from '@/api/errors';
import Navbar from '@/components/Navbar';
import { AuthContext, useAuth } from '@/hooks/auth';

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();

  const [user, setUser] = useState<model.User | null>(
    secureLocalStorage.getItem('user') as model.User
  );

  const [{ loading }, request] = useAxios(
    {},
    {
      manual: true,
    }
  );

  const updateUser = (user: model.User) => {
    secureLocalStorage.setItem('user', user);
    setUser(user);
  };

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
      updateUser(response.data.user);
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
    setUser(null);
    navigate('/sign-in', { replace: true });
  };

  const value = {
    loading,
    user,
    updateUser,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const GuestRoutes = () => {
  const { user } = useAuth();
  return !user ? <Outlet /> : <Navigate to="/" replace />;
};

export const AuthorizedRoutes = () => {
  const { user } = useAuth();
  return user ? (
    <Box display="flex" flexDirection="column" height="100dvh">
      <Navbar />
      <Outlet />
    </Box>
  ) : (
    <Navigate to="/sign-in" replace />
  );
};

export default AuthProvider;
