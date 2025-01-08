import { createContext, useContext } from 'react';

import { ErrorHandler } from '@/api/errors';

export const AuthContext = createContext<{
  loading?: boolean;
  token: string | undefined;
  user: model.User | null;
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
  token: undefined,
  user: null,
});

export const useAuth = () => {
  return useContext(AuthContext);
};
