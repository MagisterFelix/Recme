import { APIProvider, Map as GoogleMap } from '@vis.gl/react-google-maps';

const Map = () => {
  return (
    <APIProvider
      apiKey={
        import.meta.env.MODE === 'development'
          ? ''
          : import.meta.env.VITE_GOOGLE_MAP_API_KEY
      }
    >
      <GoogleMap
        defaultCenter={{ lat: 50.0152484, lng: 36.227357 }}
        defaultZoom={18}
        disableDefaultUI
      />
    </APIProvider>
  );
};

export default Map;
