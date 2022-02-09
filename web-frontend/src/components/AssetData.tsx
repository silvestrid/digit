import { useContext } from 'react';
import { useAuthUser } from 'use-eazy-auth'
import { useParams, useRouteMatch } from 'react-router-dom';

import {
    Button, Box, Grid,
    Paper, CardActions, CardContent,
    Typography,
} from '@mui/material';

import PageLoader from './PageLoader';

import useSWR from 'swr';

import fetcher from '../utils/fetcher';
import TitleContext from '../utils/titleContext';
import Chart from './MeasurementChart';
import ReportTable from './MeasurementsTable';

export default function AssetData() {
    const { token } = useAuthUser();
    const { title, setTitle } = useContext(TitleContext);
    let { siteId, assetId, monthYear } = useParams<{ siteId: string, assetId: string, monthYear: string }>();
    const { data, error } = useSWR(
        { url: `/api/abb/site/${siteId}/asset/${assetId}/`, token: token },
        fetcher
    );
    const isLoading = !error && !data;
    if (isLoading) {
        setTitle("Caricamento...");
        return <PageLoader />;
    }
    if (error) {
        setTitle("Errore");
        return <div>Error loading data...</div>
    }
    const { asset, measurements, report } = data,
        { assetName, site } = asset;
    setTitle(`${site.siteName} - ${assetName}`);
    return (
        <Grid container spacing={3}>
            {/* Chart */}
            <Grid item xs={12}>
                <Paper
                    sx={{
                        p: 2,
                        display: 'flex',
                        flexDirection: 'column',
                        height: 320,
                    }}
                >
                    <Chart data={measurements} />
                </Paper>
            </Grid>
            {/* Recent Deposits */}
            <Grid item xs={12} md={6}>
                <ReportTable data={report} />
            </Grid>
            {/* Recent Orders */}
            <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>

                </Paper>
            </Grid>
        </Grid>


    )
}