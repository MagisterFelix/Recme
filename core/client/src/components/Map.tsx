import { useNavigate, useSearchParams } from 'react-router-dom';

import {
  AdvancedMarker,
  APIProvider,
  Map as GoogleMap,
} from '@vis.gl/react-google-maps';

import { Box } from '@mui/material';

import Geolocation from '@/components/Geolocation';

const Map = ({
  recommendations,
  selectRecommendation,
}: {
  recommendations: model.Recommendation[] | undefined;
  selectRecommendation: (recommendation: model.Recommendation) => void;
}) => {
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
        {recommendations &&
          recommendations.map((recommendation) => (
            <AdvancedMarker
              key={recommendation.id}
              position={{
                lat: recommendation.location.latitude,
                lng: recommendation.location.longitude,
              }}
              onClick={() => selectRecommendation(recommendation)}
            >
              <Box
                component="img"
                src={recommendation.location.category.icon}
                alt="category"
                height={40}
                width={40}
                sx={{
                  filter:
                    'drop-shadow(1px 0 0.5px black) drop-shadow(-1px 0 0.5px black) drop-shadow(0 1px 0.5px black) drop-shadow(0 -1px 0.5px black)',
                }}
              />
            </AdvancedMarker>
          ))}
      </GoogleMap>
    </APIProvider>
  );
};

export default Map;
