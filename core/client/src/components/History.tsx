import { Fragment, useState } from 'react';

import { Box, Chip } from '@mui/material';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';

import { useAxios } from '@/api/axios';
import { ENDPOINTS } from '@/api/endpoints';
import Recommendation from '@/components/Recommendation';

const History = () => {
  const [{ loading: loadingHistory, data: history }] = useAxios<
    model.History[]
  >({
    url: ENDPOINTS.recommendations,
    method: 'GET',
  });

  const [selectedRecommendations, setSelectedRecommendations] = useState<
    model.Recommendation[]
  >([]);

  return (
    <Fragment>
      <DataGrid
        rows={history?.map((item, index) => ({
          id: index,
          filters: [
            ...item.filters.conditions.map(
              (condition) => `${condition.context}: ${condition.choice}`
            ),
            ...item.filters.preferences.map(
              (preference) => `${preference.filter}: ${preference.choice}`
            ),
          ],
          recommendations: item.recommendations.length,
        }))}
        columns={[
          {
            field: 'filters',
            headerName: 'Filters',
            flex: 3,
            sortable: false,
            renderCell: (params) => (
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, py: 1 }}>
                {params.value.map((filter: string, index: number) => (
                  <Chip
                    key={`data-grid-filter-${index}`}
                    label={filter}
                    color="primary"
                    size="small"
                  />
                ))}
              </Box>
            ),
          },
          {
            field: 'recommendations',
            headerName: 'Recommendations',
            type: 'number',
            flex: 1,
          },
        ]}
        initialState={{
          pagination: { paginationModel: { pageSize: 2 } },
        }}
        pageSizeOptions={[2]}
        rowHeight={104}
        slots={{ toolbar: GridToolbar }}
        slotProps={{ toolbar: { showQuickFilter: true } }}
        disableColumnResize
        disableColumnSelector
        disableDensitySelector
        disableColumnMenu
        disableRowSelectionOnClick
        loading={loadingHistory}
        sx={{
          p: 3,
          '&.MuiDataGrid-root .MuiDataGrid-columnHeader:focus, &.MuiDataGrid-root .MuiDataGrid-cell:focus':
            {
              outline: 'none',
            },
          '& .MuiDataGrid-row:hover': {
            cursor: 'pointer',
          },
        }}
        onRowClick={(event) =>
          setSelectedRecommendations(
            history![event.id as number].recommendations
          )
        }
      />
      {selectedRecommendations.length > 0 && (
        <Recommendation
          data={selectedRecommendations}
          close={() => setSelectedRecommendations([])}
        />
      )}
    </Fragment>
  );
};

export default History;
