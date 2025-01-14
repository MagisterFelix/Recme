import { Fragment, useEffect, useState } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { Close, FilterAlt } from '@mui/icons-material';
import { LoadingButton } from '@mui/lab';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Fab,
  FormControl,
  Grid2 as Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';

const Filter = () => {
  const [searchParams] = useSearchParams();

  const navigate = useNavigate();

  const [{ data: filters }] = useAxios<model.Filter[]>({
    url: ENDPOINTS.filters,
    method: 'GET',
  });

  const { control, setValue } = useForm();

  const [showFilters, setShowFilters] = useState(false);
  const clearFilters = () => {
    filters?.forEach((filter) => {
      setValue(filter.name, '');
    });
    navigate('/');
  };

  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (filters) {
      filters.forEach((filter) => {
        const value = searchParams.get(filter.name);
        if (value && filter.options.includes(value)) {
          setValue(filter.name, value);
        }
      });
    }
    if (!isLoaded && filters && searchParams.size) {
      setShowFilters(true);
      setIsLoaded(true);
    }
  }, [filters, searchParams, setValue, isLoaded]);

  return (
    <Fragment>
      <Fab
        color="primary"
        disabled={!filters}
        sx={{ position: 'absolute', bottom: 50, right: 50 }}
        onClick={() => setShowFilters(true)}
      >
        <FilterAlt />
      </Fab>
      <Dialog
        open={showFilters}
        fullWidth
        maxWidth="lg"
        disableEnforceFocus
        disableRestoreFocus
        onClose={() => setShowFilters(false)}
      >
        <DialogTitle>Filters</DialogTitle>
        <IconButton
          onClick={() => setShowFilters(false)}
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
          <Grid container spacing={3}>
            {filters?.map((filter) => (
              <Grid key={filter.id} size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
                <Controller
                  name={filter.name}
                  control={control}
                  defaultValue=""
                  render={({ field: { onChange, value } }) => (
                    <FormControl fullWidth>
                      <InputLabel
                        id={`filter-label-${filter.id}`}
                        sx={(theme) => ({
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1,
                          pr: 1,
                          backgroundColor: theme.palette.common.white,
                        })}
                      >
                        <Box
                          component="img"
                          src={filter.icon}
                          alt={`filter-${filter.id}`}
                          height={24}
                          width={24}
                        />
                        {filter.name}
                      </InputLabel>
                      <Select
                        label={filter.name}
                        labelId={`filter-label-${filter.id}`}
                        value={value}
                        onChange={(event) => {
                          onChange(event);
                          const { value } = event.target;
                          if (value) {
                            searchParams.set(filter.name, value);
                          } else {
                            searchParams.delete(filter.name);
                          }
                          navigate(
                            `?${decodeURIComponent(searchParams.toString())}`
                          );
                        }}
                      >
                        <MenuItem value="">
                          <em>None</em>
                        </MenuItem>
                        {filter.options.map((option) => (
                          <MenuItem value={option} key={option}>
                            {option}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  )}
                />
              </Grid>
            ))}
          </Grid>
        </DialogContent>
        <DialogActions sx={{ m: 2 }}>
          <Button
            type="submit"
            variant="outlined"
            fullWidth
            sx={{
              maxWidth: 130,
            }}
            onClick={clearFilters}
          >
            Clear
          </Button>
          <LoadingButton
            type="submit"
            variant="contained"
            fullWidth
            sx={{
              maxWidth: 130,
            }}
          >
            Apply
          </LoadingButton>
        </DialogActions>
      </Dialog>
    </Fragment>
  );
};

export default Filter;
