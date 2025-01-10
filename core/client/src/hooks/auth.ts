import { createContext, useContext } from 'react';

import { ErrorHandler } from '@/api/errors';

export const AuthContext = createContext<{
  loading?: boolean;
  user: model.User | null;
  updateUser?: (user: model.User) => void;
  login?: (
    data: request.Authorization,
    errorHandler: ErrorHandler
  ) => Promise<void>;
  register?: (
    data: request.Registration,
    errorHandler: ErrorHandler
  ) => Promise<void>;
  logout?: () => void;
}>({
  user: null,
});

export const useAuth = () => {
  return useContext(AuthContext);
};
