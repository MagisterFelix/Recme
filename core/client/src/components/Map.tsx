import { useNavigate, useSearchParams } from 'react-router-dom';

import { APIProvider, Map as GoogleMap } from '@vis.gl/react-google-maps';

import Geolocation from '@/components/Geolocation';

const Map = () => {
  const [searchParams] = useSearchParams();

  const navigate = useNavigate();

  const pickGeolocation = (latLng: google.maps.LatLngLiteral) => {
    searchParams.set('latitude', latLng.lat.toString());
    searchParams.set('longitude', latLng.lng.toString());
    navigate(`?${decodeURIComponent(searchParams.toString())}`);
  };

  return (
    <APIProvider
      apiKey={
        import.meta.env.MODE === 'development'
          ? ''
          : import.meta.env.VITE_GOOGLE_MAP_API_KEY
      }
    >
      <GoogleMap
        mapId={'GOOGLE_MAP_ID'}
        defaultCenter={{ lat: 50.0152484, lng: 36.227357 }}
        defaultZoom={18}
        disableDefaultUI
        onClick={(event) => pickGeolocation(event.detail.latLng!)}
      >
        <Geolocation />
      </GoogleMap>
    </APIProvider>
  );
};

export default Map;
