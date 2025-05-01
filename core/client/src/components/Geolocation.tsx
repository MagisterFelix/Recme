import { Fragment, useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { LocationDisabled, MyLocation } from '@mui/icons-material';
import { Fab } from '@mui/material';

const Geolocation = () => {
  const [searchParams] = useSearchParams();

  const navigate = useNavigate();

  const [geolocation, setGeolocation] = useState<{
    latitude: number;
    longitude: number;
  } | null>(null);

  const getGeolocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setGeolocation({ latitude, longitude });
          searchParams.set('latitude', latitude.toString());
          searchParams.set('longitude', longitude.toString());
          navigate(`?${decodeURIComponent(searchParams.toString())}`);
        },
        (error) => {
          alert(`Unable to retrieve your location: ${error.message}.`);
        }
      );
    } else {
      alert('Geolocation is not supported.');
    }
  };

  const resetGeolocation = () => {
    setGeolocation(null);
    searchParams.delete('latitude');
    searchParams.delete('longitude');
    navigate(`?${decodeURIComponent(searchParams.toString())}`);
  };

  useEffect(() => {
    if (searchParams.has('latitude') || searchParams.has('longitude')) {
      const latitude = Number(searchParams.get('latitude') || NaN);
      const longitude = Number(searchParams.get('longitude') || NaN);

      if (
        latitude >= -90 &&
        latitude <= 90 &&
        longitude >= -180 &&
        longitude <= 180
      ) {
        setGeolocation({ latitude, longitude });
      } else {
        setGeolocation(null);
        navigate(`?${decodeURIComponent(new URLSearchParams().toString())}`);
      }
    }
  }, [searchParams, navigate]);

  return (
    <Fragment>
      {geolocation ? (
        <Fab
          color="warning"
          sx={{ position: 'absolute', bottom: 125, right: 50 }}
          onClick={resetGeolocation}
        >
          <LocationDisabled />
        </Fab>
      ) : (
        <Fab
          color="primary"
          sx={{ position: 'absolute', bottom: 125, right: 50 }}
          onClick={getGeolocation}
        >
          <MyLocation />
        </Fab>
      )}
    </Fragment>
  );
};

export default Geolocation;
