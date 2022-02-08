import { useContext } from 'react';
import { useAuthUser } from 'use-eazy-auth'
import { useRouteMatch, Link } from 'react-router-dom';

import {
    Button, Grid,
    Card, CardHeader, CardActions, CardContent,
    Typography,
} from '@mui/material';

import PageLoader from './PageLoader';
import fetcher from '../utils/fetcher';
import TitleContext from '../utils/titleContext';

import useSWR from 'swr';

type Site = {
    siteId: string;
    siteName: string;
    country: string;
    countryCode: string;
    address: string;
    city: string;
    latitude: string;
    longitude: string;
}

function capitalizeFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}


function SiteCard({ site }: { site: Site }) {
    let { url } = useRouteMatch();
    return (
        <Card>
            <CardHeader
                title={capitalizeFirstLetter(site.siteName)}
                subheader={`Id: ${site.siteId}`}
            />
            <CardContent>
                <Typography variant="body2" color="textSecondary" component="p">
                    {site.address}, {site.city}, {site.countryCode}
                </Typography>
            </CardContent>
            <CardActions>
                <Link to={`${url}/${site.siteId}`} style={{ textDecoration: 'none' }}>
                    <Button size="small">Scegli Asset</Button>
                </Link>
            </CardActions>
        </Card>
    );
}

function compare(siteA: Site, siteB: Site) {
    const a = siteA.siteName.toLowerCase(), b = siteB.siteName.toLowerCase();
    if (a < b) {
        return -1;
    }
    if (a > b) {
        return 1;
    }
    return 0;
}

export default function SiteGrid() {
    const { token } = useAuthUser();
    const { title, setTitle } = useContext(TitleContext);
    const { data, error } = useSWR(
        { url: "/api/abb/site/", token: token },
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
    setTitle("Siti disponibili")
    return (
        <Grid container spacing={3}>
            {data.sites.sort(compare).map((site: Site) =>
                <Grid item xs={12} md={6} key={site.siteId}>
                    <SiteCard site={site} />
                </Grid>
            )}
        </Grid>
    );
}