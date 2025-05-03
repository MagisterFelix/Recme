import { Fragment, useState } from 'react';

import { LinearProgress } from '@mui/material';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';
import Filter from '@/components/Filter';
import Geolocation from '@/components/Geolocation';
import Map from '@/components/Map';
import Recommendation from '@/components/Recommendation';

const Home = () => {
  const [{ loading: loadingRecommendations }, request] = useAxios<
    model.Recommendation[]
  >(
    {
      url: ENDPOINTS.recommendations,
      method: 'GET',
    },
    {
      manual: true,
    }
  );

  const getRecommendations = async (params: object) => {
    await request({ params });
  };

  const [selectedRecommendations, setSelectedRecommendations] = useState<
    model.Recommendation[]
  >([]);

  return (
    <Fragment>
      {loadingRecommendations && <LinearProgress />}
      <Map />
      {selectedRecommendations.length > 0 && (
        <Recommendation
          data={selectedRecommendations}
          close={() => setSelectedRecommendations([])}
        />
      )}
      <Geolocation />
      <Filter getRecommendations={getRecommendations} />
    </Fragment>
  );
};

export default Home;
