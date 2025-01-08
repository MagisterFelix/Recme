import { Button, Container } from '@mui/material';

import { useAuth } from '@/hooks/auth';

const Home = () => {
  const { logout } = useAuth();

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
      <Button variant="contained" onClick={logout}>
        Logout
      </Button>
    </Container>
  );
};

export default Home;
