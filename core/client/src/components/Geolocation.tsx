import { Fragment, useEffect, useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { AdvancedMarker, useMap } from '@vis.gl/react-google-maps';

import { LocationDisabled, MyLocation } from '@mui/icons-material';
import { Box, Fab } from '@mui/material';

import position from '@/static/geolocation.svg';

const Geolocation = ({
  loadingRecommendations,
}: {
  loadingRecommendations: boolean;
}) => {
  const [searchParams] = useSearchParams();

  const navigate = useNavigate();

  const map = useMap();

  const circleRef = useRef<google.maps.Circle | null>(null);

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
    if (!map) {
      return;
    }

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
        map.panTo({ lat: latitude, lng: longitude });
        if (map.getZoom() != 18) {
          map.setZoom(18);
        }
      } else {
        setGeolocation(null);
        navigate(`?${decodeURIComponent(new URLSearchParams().toString())}`);
      }
    }
  }, [searchParams, navigate, map]);

  useEffect(() => {
    if (!map || !geolocation) {
      return;
    }

    if (circleRef.current) {
      circleRef.current.setMap(null);
      circleRef.current = null;
    }

    if (!loadingRecommendations) {
      return;
    }

    map.panTo({ lat: geolocation.latitude, lng: geolocation.longitude });
    if (map.getZoom() != 15) {
      map.setZoom(15);
    }

    const circleOptions: google.maps.CircleOptions = {
      map: map,
      center: { lat: geolocation.latitude, lng: geolocation.longitude },
      radius: 1000,
      strokeColor: '#0c4cb3',
      strokeOpacity: 0.8,
      strokeWeight: 3,
      fillColor: '#3b82f6',
      fillOpacity: 0.2,
    };

    circleRef.current = new google.maps.Circle(circleOptions);

    let opacity = 0;
    let direction = 1;
    const step = 0.01;
    const minOpacity = 0.2;
    const maxOpacity = 0.5;

    const animate = () => {
      if (!circleRef.current) {
        return;
      }

      opacity += direction * step;

      if (opacity >= maxOpacity) {
        opacity = maxOpacity;
        direction = -1;
      } else if (opacity <= minOpacity) {
        opacity = minOpacity;
        direction = 1;
      }

      circleRef.current.setOptions({ fillOpacity: opacity });

      requestAnimationFrame(animate);
    };

    animate();

    return () => {
      map.panTo({ lat: geolocation.latitude, lng: geolocation.longitude });
      if (map.getZoom() != 15) {
        map.setZoom(15);
      }

      if (circleRef.current) {
        circleRef.current.setMap(null);
        circleRef.current = null;
      }
    };
  }, [map, geolocation, loadingRecommendations]);

  return (
    <Fragment>
      {geolocation ? (
        <Fragment>
          <Fab
            color="warning"
            disabled={loadingRecommendations}
            sx={{ position: 'absolute', bottom: 125, right: 50 }}
            onClick={resetGeolocation}
          >
            <LocationDisabled />
          </Fab>
          <AdvancedMarker
            anchorPoint={['50%', '70%']}
            position={{ lat: geolocation.latitude, lng: geolocation.longitude }}
          >
            <Box
              component="img"
              src={position}
              alt="position"
              height={80}
              width={80}
              sx={{
                filter:
                  'drop-shadow(1px 0 0.5px black) drop-shadow(-1px 0 0.5px black) drop-shadow(0 1px 0.5px black) drop-shadow(0 -1px 0.5px black)',
              }}
            />
          </AdvancedMarker>
        </Fragment>
      ) : (
        <Fab
          color="primary"
          disabled={loadingRecommendations}
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
