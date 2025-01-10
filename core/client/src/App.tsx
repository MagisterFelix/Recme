import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';

import Authorization from '@/pages/Authorization';
import Home from '@/pages/Home';
import Profile from '@/pages/Profile';
import Registration from '@/pages/Registration';
import AuthProvider, { AuthorizedRoutes, GuestRoutes } from '@/providers/auth';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route element={<GuestRoutes />}>
              <Route path="/sign-in" element={<Authorization />} />
              <Route path="/sign-up" element={<Registration />} />
            </Route>
            <Route element={<AuthorizedRoutes />}>
              <Route path="/" element={<Home />} />
              <Route path="/profile" element={<Profile />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
};

export default App;
