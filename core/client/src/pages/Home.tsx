import { Fragment, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import { LinearProgress } from '@mui/material';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';
import Filter from '@/components/Filter';
import Map from '@/components/Map';
import Recommendation from '@/components/Recommendation';

const Home = () => {
  const [searchParams] = useSearchParams();

  const [recommendations, setRecommendations] = useState<
    model.Recommendation[]
  >([]);

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

  const getRecommendations = async (data: object) => {
    setRecommendations([]);
    const params = {
      latitude: searchParams.get('latitude'),
      longitude: searchParams.get('longitude'),
      ...data,
    };
    const response = await request({ params });
    setRecommendations(response.data);
  };

  const [selectedRecommendation, setSelectedRecommendation] =
    useState<model.Recommendation | null>(null);

  const selectRecommendation = (recommendation: model.Recommendation) => {
    setSelectedRecommendation(recommendation);
  };

  return (
    <Fragment>
      {loadingRecommendations && <LinearProgress />}
      <Map
        recommendations={recommendations}
        selectRecommendation={selectRecommendation}
        loadingRecommendations={loadingRecommendations}
      />
      {selectedRecommendation && (
        <Recommendation
          data={[selectedRecommendation]}
          close={() => setSelectedRecommendation(null)}
        />
      )}
      <Filter
        getRecommendations={getRecommendations}
        loadingRecommendations={loadingRecommendations}
      />
    </Fragment>
  );
};

export default Home;
