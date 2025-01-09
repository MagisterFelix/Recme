import { useState } from 'react';

import { AccountCircle, ExitToApp } from '@mui/icons-material';
import {
  AppBar,
  Avatar,
  Box,
  Container,
  IconButton,
  Link,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material';

import { useAuth } from '@/hooks/auth';
import logo from '@/static/logo.svg';

const Navbar = () => {
  const theme = useTheme();
  const underSm = useMediaQuery(useTheme().breakpoints.down('sm'));

  const { user, logout } = useAuth();

  const [anchorElUser, setAnchorElUser] = useState<HTMLElement | null>(null);

  return (
    <AppBar position="sticky" sx={{ bgcolor: '#202329' }}>
      <Container maxWidth="xl">
        <Toolbar
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          <Link
            href="/"
            display="flex"
            alignItems="center"
            textTransform="uppercase"
            underline="none"
            fontSize="1.5rem"
            fontWeight="bold"
            color={theme.palette.common.white}
          >
            <Box
              component="img"
              src={logo}
              alt="logo"
              py={2}
              height={72}
              width={72}
            />
            <Typography
              display={underSm ? 'none' : 'flex'}
              textTransform="uppercase"
              fontSize="1.25rem"
              fontWeight="bold"
            >
              Recme
            </Typography>
          </Link>
          <Box display="flex" alignItems="center">
            <Typography
              display={underSm ? 'none' : 'flex'}
              fontSize="1.25rem"
              fontWeight="bold"
              pr={1}
            >
              {user?.name}
            </Typography>
            <IconButton
              onClick={(event) => setAnchorElUser(event.currentTarget)}
              sx={{ pr: 1.5 }}
            >
              <Avatar
                src={user?.image}
                alt={user?.name}
                sx={{
                  height: 48,
                  width: 48,
                }}
              />
            </IconButton>
            <Menu
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'center',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'center',
              }}
              open={Boolean(anchorElUser)}
              onClose={() => setAnchorElUser(null)}
            >
              <MenuItem>
                <Link
                  href="/profile"
                  display="flex"
                  alignItems="center"
                  underline="none"
                  color={theme.palette.common.black}
                >
                  <AccountCircle sx={{ mt: -0.25, mr: 1 }} />
                  Profile
                </Link>
              </MenuItem>
              <MenuItem onClick={logout}>
                <Typography
                  display="flex"
                  alignItems="center"
                  color={theme.palette.common.black}
                >
                  <ExitToApp sx={{ mr: 1 }} />
                  Logout
                </Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;
