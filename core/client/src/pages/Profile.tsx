import { useState } from 'react';
import { Controller, useForm } from 'react-hook-form';

import { AxiosError, AxiosResponse } from 'axios';

import {
  AccountCircle,
  Email,
  EnhancedEncryption,
  Image,
  Key,
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
  Paper,
  TextField,
  Typography,
} from '@mui/material';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';
import { ErrorData, handleErrors } from '@/api/errors';
import { useAuth } from '@/hooks/auth';

const Profile = () => {
  const { user, updateUser } = useAuth();

  const validationUser = {
    name: {
      required: 'This field may not be blank.',
      maxLength: 'No more than 150 characters.',
    },
    email: {
      required: 'This field may not be blank.',
      maxLength: 'No more than 150 characters.',
      pattern: 'Provide the valid email.',
    },
    image: {
      validate: 'Invalid image or size greater than 10 MB.',
    },
  };

  const [{ loading: loadingEditUser }, editUser] = useAxios(
    {
      url: ENDPOINTS.user,
      method: 'PATCH',
    },
    {
      manual: true,
    }
  );

  const [alertUser, setAlertUser] = useState<{
    type: AlertColor;
    message: string;
  } | null>(null);
  const {
    control: controlUser,
    handleSubmit: handleSubmitUser,
    setError: setErrorUser,
    reset: resetUser,
  } = useForm();
  const handleOnSubmitUser = async (data: request.UserUpdating) => {
    setAlertUser(null);
    const formData = Object.entries(data).filter(
      ([key, value]) => user && user[key as keyof model.User] !== value
    );
    if (formData.length === 0) {
      setAlertUser({ type: 'info', message: 'Nothing to update.' });
    } else {
      const errorHandler = {
        validation: validationUser,
        setError: setErrorUser,
        setAlert: setAlertUser,
      };
      try {
        const response: AxiosResponse<model.User> = await editUser({
          data: Object.fromEntries(formData),
        });
        resetUser({
          name: response.data.name,
          email: response.data.email,
          image: response.data.image,
        });
        updateUser!(response.data);
        setAlertUser({ type: 'success', message: 'User has been updated.' });
      } catch (err) {
        const error = (err as AxiosError).response?.data as ErrorData;
        handleErrors(error.details, errorHandler);
      }
    }
  };

  const validationPassword = {
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

  const [{ loading: loadingChangePassword }, changePassword] = useAxios(
    {
      url: ENDPOINTS.user,
      method: 'PATCH',
    },
    {
      manual: true,
    }
  );

  const [alertPassword, setAlertPassword] = useState<{
    type: AlertColor;
    message: string;
  } | null>(null);
  const {
    control: controlPassword,
    watch: watchPassword,
    handleSubmit: handleSubmitPassword,
    setError: setErrorPassword,
  } = useForm();
  const handleOnSubmitPassword = async (data: request.PasswordChanging) => {
    setAlertPassword(null);
    const errorHandler = {
      validation: validationPassword,
      setError: setErrorPassword,
      setAlert: setAlertPassword,
    };
    try {
      await changePassword({
        data,
      });
      setAlertPassword({
        type: 'success',
        message: 'Password has been changed.',
      });
    } catch (err) {
      const error = (err as AxiosError).response?.data as ErrorData;
      handleErrors(error.details, errorHandler);
    }
  };

  const [showPassword, setShowPassword] = useState(false);
  const handleClickShowPassword = () => setShowPassword((show) => !show);

  return (
    <Container sx={{ my: 2 }}>
      <Grid
        container
        sx={{
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <Grid size={{ xs: 12, md: 8 }} p={2}>
          <Paper elevation={6}>
            <Grid p={3}>
              <Grid container>
                <Typography
                  display="flex"
                  alignItems="center"
                  fontSize="2rem"
                  fontWeight="bold"
                  margin="auto"
                >
                  User
                </Typography>
              </Grid>
              <Grid mt={1} textAlign="right">
                <Box component="form" autoComplete="off">
                  <Controller
                    name="name"
                    control={controlUser}
                    defaultValue={user?.name}
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
                            startAdornment: (
                              <InputAdornment position="start">
                                <AccountCircle />
                              </InputAdornment>
                            ),
                          },
                        }}
                        error={fieldError !== undefined}
                        helperText={
                          fieldError
                            ? fieldError.message ||
                              validationUser.name[
                                fieldError.type as keyof typeof validationUser.name
                              ]
                            : ''
                        }
                      />
                    )}
                  />
                  <Controller
                    name="email"
                    control={controlUser}
                    defaultValue={user?.email}
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
                            startAdornment: (
                              <InputAdornment position="start">
                                <Email />
                              </InputAdornment>
                            ),
                          },
                        }}
                        error={fieldError !== undefined}
                        helperText={
                          fieldError
                            ? fieldError.message ||
                              validationUser.email[
                                fieldError.type as keyof typeof validationUser.email
                              ]
                            : ''
                        }
                      />
                    )}
                  />
                  <Controller
                    name="image"
                    control={controlUser}
                    defaultValue={user?.image}
                    rules={{
                      validate: (file) =>
                        file &&
                        file.type &&
                        file.type.startsWith('image/') &&
                        file.size / (1024 * 1024) <= 10,
                    }}
                    render={({
                      field: { onChange, value },
                      fieldState: { error: fieldError },
                    }) => (
                      <TextField
                        onChange={(event) => {
                          const target = event.target as HTMLInputElement;
                          if (target.files && target.files[0]) {
                            onChange(target.files[0]);
                          }
                        }}
                        value={value && value.filename}
                        fullWidth
                        margin="dense"
                        type="file"
                        label="Image"
                        slotProps={{
                          inputLabel: {
                            shrink: true,
                          },
                          input: {
                            startAdornment: (
                              <InputAdornment position="start">
                                <Image />
                              </InputAdornment>
                            ),
                          },
                          htmlInput: {
                            accept: 'image/*',
                            style: { cursor: 'pointer' },
                          },
                        }}
                        error={fieldError !== undefined}
                        helperText={
                          fieldError
                            ? fieldError.message ||
                              validationUser.image[
                                fieldError.type as keyof typeof validationUser.image
                              ]
                            : ''
                        }
                        sx={{
                          '& input[type="file"]::file-selector-button': {
                            display: 'none',
                          },
                        }}
                      />
                    )}
                  />
                  {alertUser && (
                    <Alert
                      severity={alertUser.type}
                      sx={{ textAlign: 'left', my: 1 }}
                    >
                      {alertUser.message}
                    </Alert>
                  )}
                  <LoadingButton
                    type="submit"
                    variant="contained"
                    fullWidth
                    loading={loadingEditUser}
                    sx={{
                      mt: 2,
                      maxWidth: 125,
                    }}
                    onClick={handleSubmitUser((data: object) =>
                      handleOnSubmitUser(data as request.UserUpdating)
                    )}
                  >
                    Update
                  </LoadingButton>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }} p={2}>
          <Paper elevation={6}>
            <Grid p={3}>
              <Grid container>
                <Typography
                  display="flex"
                  alignItems="center"
                  fontSize="2rem"
                  fontWeight="bold"
                  margin="auto"
                >
                  Password
                </Typography>
              </Grid>
              <Grid mt={1} textAlign="right">
                <Box component="form" autoComplete="off">
                  <Controller
                    name="password"
                    control={controlPassword}
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
                        label="Old password"
                        slotProps={
                          value
                            ? {
                                input: {
                                  startAdornment: (
                                    <InputAdornment position="start">
                                      <Key />
                                    </InputAdornment>
                                  ),
                                },
                              }
                            : {}
                        }
                        error={fieldError !== undefined}
                        helperText={
                          fieldError
                            ? fieldError.message ||
                              validationPassword.password[
                                fieldError.type as keyof typeof validationPassword.password
                              ]
                            : ''
                        }
                      />
                    )}
                  />
                  <Controller
                    name="new_password"
                    control={controlPassword}
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
                        label="New password"
                        slotProps={
                          value
                            ? {
                                input: {
                                  startAdornment: (
                                    <InputAdornment position="start">
                                      <EnhancedEncryption />
                                    </InputAdornment>
                                  ),
                                  endAdornment: (
                                    <InputAdornment position="end">
                                      <IconButton
                                        onClick={handleClickShowPassword}
                                        onMouseDown={(event) =>
                                          event.preventDefault()
                                        }
                                        onMouseUp={(event) =>
                                          event.preventDefault()
                                        }
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
                              }
                            : {}
                        }
                        error={fieldError !== undefined}
                        helperText={
                          fieldError
                            ? fieldError.message ||
                              validationPassword.password[
                                fieldError.type as keyof typeof validationPassword.password
                              ]
                            : ''
                        }
                      />
                    )}
                  />
                  <Controller
                    name="confirm_password"
                    control={controlPassword}
                    defaultValue=""
                    rules={{
                      required: true,
                      validate: (password) =>
                        password === watchPassword('new_password'),
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
                        label="Confirm new password"
                        slotProps={
                          value
                            ? {
                                input: {
                                  startAdornment: (
                                    <InputAdornment position="start">
                                      <Lock />
                                    </InputAdornment>
                                  ),
                                },
                              }
                            : {}
                        }
                        error={fieldError !== undefined}
                        helperText={
                          fieldError
                            ? fieldError.message ||
                              validationPassword.confirm_password[
                                fieldError.type as keyof typeof validationPassword.confirm_password
                              ]
                            : ''
                        }
                      />
                    )}
                  />
                  {alertPassword && (
                    <Alert
                      severity={alertPassword.type}
                      sx={{ textAlign: 'left', my: 1 }}
                    >
                      {alertPassword.message}
                    </Alert>
                  )}
                  <LoadingButton
                    type="submit"
                    variant="contained"
                    fullWidth
                    loading={loadingChangePassword}
                    sx={{
                      mt: 2,
                      maxWidth: 125,
                    }}
                    onClick={handleSubmitPassword((data: object) =>
                      handleOnSubmitPassword(data as request.PasswordChanging)
                    )}
                  >
                    Change
                  </LoadingButton>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Profile;
