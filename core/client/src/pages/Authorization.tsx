import { useState } from 'react';
import { Controller, useForm } from 'react-hook-form';

import { Email, Visibility, VisibilityOff } from '@mui/icons-material';
import { LoadingButton } from '@mui/lab';
import {
  Alert,
  AlertColor,
  Box,
  Container,
  Grid2 as Grid,
  IconButton,
  InputAdornment,
  Link,
  Paper,
  TextField,
  Typography,
} from '@mui/material';

import { useAuth } from '@/hooks/auth';
import logo from '@/static/logo.svg';

const Authorization = () => {
  const { loading, login } = useAuth();

  const validation = {
    email: {
      required: 'This field may not be blank.',
    },
    password: {
      required: 'This field may not be blank.',
    },
  };

  const [alert, setAlert] = useState<{
    type: AlertColor;
    message: string;
  } | null>(null);
  const { control, handleSubmit, setError } = useForm();
  const handleOnSubmit = async (data: request.Authorization) => {
    setAlert(null);
    const errorHandler = {
      validation,
      setError,
      setAlert,
    };
    await login!(data, errorHandler);
  };

  const [showPassword, setShowPassword] = useState(false);
  const handleClickShowPassword = () => setShowPassword((show) => !show);

  return (
    <Container
      maxWidth="md"
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        verticalAlign: 'center',
        minHeight: '100dvh',
      }}
    >
      <Paper elevation={6}>
        <Grid>
          <Grid p={4}>
            <Grid>
              <Typography
                display="flex"
                alignItems="center"
                textTransform="uppercase"
                fontSize="2rem"
                fontWeight="bold"
              >
                <Box
                  component="img"
                  src={logo}
                  alt="logo"
                  mr={1}
                  height={64}
                  width={64}
                />
                Recme
              </Typography>
            </Grid>
            <Grid my={3}>
              <Typography textTransform="uppercase" fontWeight="bold">
                Sign In
              </Typography>
              <Typography>To use the system</Typography>
            </Grid>
            <Grid textAlign="center">
              <Box component="form" autoComplete="off">
                <Controller
                  name="email"
                  control={control}
                  defaultValue=""
                  rules={{
                    required: true,
                  }}
                  render={({
                    field: { onChange, value },
                    fieldState: { error: fieldError },
                  }) => (
                    <TextField
                      onChange={onChange}
                      value={value}
                      required
                      fullWidth
                      margin="dense"
                      type="text"
                      label="Email"
                      slotProps={{
                        input: {
                          endAdornment: (
                            <InputAdornment position="end">
                              <Email />
                            </InputAdornment>
                          ),
                        },
                      }}
                      error={fieldError !== undefined}
                      helperText={
                        fieldError
                          ? fieldError.message ||
                            validation.email[
                              fieldError.type as keyof typeof validation.email
                            ]
                          : ''
                      }
                    />
                  )}
                />
                <Controller
                  name="password"
                  control={control}
                  defaultValue=""
                  rules={{
                    required: true,
                  }}
                  render={({
                    field: { onChange, value },
                    fieldState: { error: fieldError },
                  }) => (
                    <TextField
                      onChange={onChange}
                      value={value}
                      required
                      fullWidth
                      margin="dense"
                      type={showPassword ? 'text' : 'password'}
                      label="Password"
                      slotProps={{
                        input: {
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                onClick={handleClickShowPassword}
                                onMouseDown={(event) => event.preventDefault()}
                                onMouseUp={(event) => event.preventDefault()}
                                edge="end"
                                sx={{ mr: -1 }}
                              >
                                {showPassword ? (
                                  <VisibilityOff />
                                ) : (
                                  <Visibility />
                                )}
                              </IconButton>
                            </InputAdornment>
                          ),
                        },
                      }}
                      error={fieldError !== undefined}
                      helperText={
                        fieldError
                          ? fieldError.message ||
                            validation.password[
                              fieldError.type as keyof typeof validation.password
                            ]
                          : ''
                      }
                    />
                  )}
                />
                {alert && (
                  <Alert
                    severity={alert.type}
                    sx={{ textAlign: 'left', my: 1 }}
                  >
                    {alert.message}
                  </Alert>
                )}
                <Typography display="block" my={3}>
                  Don't have an account?&nbsp;
                  <Link href="/sign-up" underline="hover">
                    Sign&nbsp;Up
                  </Link>
                </Typography>
                <LoadingButton
                  type="submit"
                  variant="contained"
                  fullWidth
                  loading={loading}
                  sx={{
                    maxWidth: 300,
                  }}
                  onClick={handleSubmit((data: object) =>
                    handleOnSubmit(data as request.Authorization)
                  )}
                >
                  Sign In
                </LoadingButton>
              </Box>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Authorization;
