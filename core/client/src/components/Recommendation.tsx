import { useState } from 'react';

import { AxiosResponse } from 'axios';

import {
  Close,
  SentimentSatisfiedAlt,
  SentimentVeryDissatisfied,
} from '@mui/icons-material';
import {
  Box,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid2 as Grid,
  IconButton,
  Pagination,
  Rating,
  Typography,
  useMediaQuery,
  useTheme,
} from '@mui/material';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';

const Recommendation = ({
  data,
  close,
}: {
  data: model.Recommendation[];
  close: () => void;
}) => {
  const theme = useTheme();

  const underSm = useMediaQuery(theme.breakpoints.down('sm'));

  const [currentRecommendation, setCurrentRecommendation] = useState(0);

  const [{ loading }, request] = useAxios(
    {},
    {
      manual: true,
    }
  );

  const [rating, setRating] = useState<number | null>(
    data[currentRecommendation].location.rating.user
  );
  const review = async (reqData: request.Reviewing) => {
    const response: AxiosResponse<model.Review> = await request({
      url: ENDPOINTS.reviews,
      method: 'POST',
      data: reqData,
    });
    data[currentRecommendation].location = response.data.location;
  };

  const [isLiked, setIsLiked] = useState<boolean | null>(
    data[currentRecommendation].is_liked
  );
  const estimate = async (reqData: request.Estimating) => {
    const response: AxiosResponse<model.Recommendation> = await request({
      url: `${ENDPOINTS.recommendation}${data[currentRecommendation].id}/`,
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      data: reqData,
    });
    data[currentRecommendation] = response.data;
  };

  return (
    <Dialog
      open={data.length !== 0}
      fullWidth
      maxWidth="md"
      disableEnforceFocus
      disableRestoreFocus
      onClose={close}
    >
      <DialogTitle>Recommendation</DialogTitle>
      <IconButton
        onClick={close}
        sx={(theme) => ({
          position: 'absolute',
          right: 8,
          top: 8,
          color: theme.palette.grey[500],
        })}
      >
        <Close />
      </IconButton>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid size={12}>
            <Typography variant="subtitle2">Filters:</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, py: 1 }}>
              {data
                .flatMap((item) => [
                  ...item.filters.conditions.map(
                    (condition) => `${condition.context}: ${condition.choice}`
                  ),
                  ...item.filters.preferences.map(
                    (preference) => `${preference.filter}: ${preference.choice}`
                  ),
                ])
                .map((filter, index) => (
                  <Chip
                    key={`filter-${index}`}
                    label={filter}
                    color="primary"
                    size="small"
                  />
                ))}
            </Box>
          </Grid>
          <Grid size={12}>
            <Typography variant="subtitle2">Location:</Typography>
            <Typography>{data[currentRecommendation].location.name}</Typography>
            <Box
              component="img"
              src={data[currentRecommendation].location.image}
              alt={data[currentRecommendation].location.name}
              maxHeight={256}
              maxWidth="100%"
            />
          </Grid>
          <Grid size={12}>
            <Typography variant="subtitle2">Category:</Typography>
            <Box display="flex" alignItems="center">
              <Box
                component="img"
                src={data[currentRecommendation].location.category.icon}
                alt={data[currentRecommendation].location.category.name}
                height={32}
                width={32}
              />
              &nbsp;
              <Typography>
                {data[currentRecommendation].location.category.name}
              </Typography>
            </Box>
          </Grid>
          <Grid size={12}>
            <Typography variant="subtitle2">Rating:</Typography>
            <Rating
              size="large"
              value={data[currentRecommendation].location.rating.avg}
              readOnly
            />
          </Grid>
        </Grid>
        <DialogContentText textAlign="right">
          {new Date(data[currentRecommendation].created_at).toDateString()}
        </DialogContentText>
      </DialogContent>
      <DialogActions
        sx={{
          m: 1,
          gap: 2,
          display: 'flex',
          justifyContent: data.length > 1 ? 'space-between' : 'end',
          flexDirection: {
            xs: 'column',
            md: 'row',
          },
        }}
      >
        {data.length > 1 && (
          <Pagination
            count={data.length}
            color="primary"
            shape="rounded"
            siblingCount={underSm ? 0 : 1}
            boundaryCount={underSm ? 0 : 1}
            onChange={(_, page) => {
              setCurrentRecommendation(page - 1);
              setRating(data[page - 1].location.rating.user);
              setIsLiked(data[page - 1].is_liked);
            }}
          />
        )}
        <Box
          sx={{
            gap: 1,
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <Rating
            size="large"
            disabled={loading}
            value={rating}
            onChange={(_, value) => {
              if (value === null) {
                return;
              }
              setRating(value);
              review({
                location: data[currentRecommendation].location.id,
                rating: value,
              });
            }}
          />
          <Rating
            max={2}
            size="large"
            disabled={loading}
            value={isLiked === false ? 1 : isLiked === true ? 2 : null}
            highlightSelectedOnly
            IconContainerComponent={({ value, ...other }) => {
              return (
                <span {...other}>
                  {value === 1 ? (
                    <SentimentVeryDissatisfied color="error" fontSize="large" />
                  ) : (
                    <SentimentSatisfiedAlt color="success" fontSize="large" />
                  )}
                </span>
              );
            }}
            sx={{
              '& .MuiRating-iconEmpty .MuiSvgIcon-root': {
                color: theme.palette.action.disabled,
              },
            }}
            onChange={(_, value) => {
              if (value === 1) {
                setIsLiked(false);
                estimate({
                  is_liked: false,
                });
              } else if (value === 2) {
                setIsLiked(true);
                estimate({
                  is_liked: true,
                });
              } else {
                setIsLiked(null);
                estimate({
                  is_liked: null,
                });
              }
            }}
          />
        </Box>
      </DialogActions>
    </Dialog>
  );
};

export default Recommendation;
