import { useState } from 'react';
import { Controller, useForm } from 'react-hook-form';

import {
  AccountCircle,
  Email,
  Lock,
  Visibility,
  VisibilityOff,
} from '@mui/icons-material';
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

const Registration = () => {
  const { loading, register } = useAuth();

  const validation = {
    name: {
      required: 'This field may not be blank.',
      maxLength: 'No more than 150 characters.',
    },
    email: {
      required: 'This field may not be blank.',
      maxLength: 'No more than 150 characters.',
      pattern: 'Provide the valid email.',
    },
    password: {
      required: 'This field may not be blank.',
      minLength: 'At least 8 characters.',
      maxLength: 'No more than 128 characters.',
      pattern: 'Provide the valid password.',
    },
    confirm_password: {
      required: 'This field may not be blank.',
      validate: 'Password mismatch.',
    },
  };

  const [alert, setAlert] = useState<{
    type: AlertColor;
    message: string;
  } | null>(null);
  const { control, handleSubmit, setError, watch } = useForm();
  const handleOnSubmit = async (data: request.Registration) => {
    setAlert(null);
    const errorHandler = {
      validation,
      setError,
      setAlert,
    };
    await register!(data, errorHandler);
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
                Sign Up
              </Typography>
              <Typography>To use the system</Typography>
            </Grid>
            <Grid textAlign="center">
              <Box component="form" autoComplete="off">
                <Controller
                  name="name"
                  control={control}
                  defaultValue=""
                  rules={{
                    required: true,
                    maxLength: 150,
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
                      label="Name"
                      slotProps={{
                        input: {
                          endAdornment: (
                            <InputAdornment position="end">
                              <AccountCircle />
                            </InputAdornment>
                          ),
                        },
                      }}
                      error={fieldError !== undefined}
                      helperText={
                        fieldError
                          ? fieldError.message ||
                            validation.name[
                              fieldError.type as keyof typeof validation.name
                            ]
                          : ''
                      }
                    />
                  )}
                />
                <Controller
                  name="email"
                  control={control}
                  defaultValue=""
                  rules={{
                    required: true,
                    maxLength: 150,
                    pattern: /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/,
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
                    minLength: 8,
                    maxLength: 128,
                    pattern: /^(?=.*\d)(?=.*[A-Za-z]).{8,128}$/,
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
                <Controller
                  name="confirm_password"
                  control={control}
                  defaultValue=""
                  rules={{
                    required: true,
                    validate: (password) => password === watch('password'),
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
                      label="Confirm password"
                      slotProps={{
                        input: {
                          endAdornment: (
                            <InputAdornment position="end">
                              <Lock />
                            </InputAdornment>
                          ),
                        },
                      }}
                      error={fieldError !== undefined}
                      helperText={
                        fieldError
                          ? fieldError.message ||
                            validation.confirm_password[
                              fieldError.type as keyof typeof validation.confirm_password
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
                  Already have an account?&nbsp;
                  <Link href="/sign-in" underline="hover">
                    Sign&nbsp;In
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
                    handleOnSubmit(data as request.Registration)
                  )}
                >
                  Sign Up
                </LoadingButton>
              </Box>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Registration;
