import { useContext } from 'react';
import { useAuthUser } from 'use-eazy-auth';
import { useParams, useRouteMatch, Link } from 'react-router-dom';

import {
    Button, Grid,
    Card, CardHeader, CardActions, CardContent,
    Typography,
} from '@mui/material';

import PageLoader from './PageLoader';
import fetcher from '../utils/fetcher';
import TitleContext from '../utils/titleContext';

import useSWR from 'swr';

type MotionAsset = {
    motionAssetId: string;
    assetId: string;
    assetTypeId: string;
    assetTypeVersion: string;
    assetType: string;
    assetFamily: string;
    assetName: string;
    baseAPI: number;
    description: string;
    site: {
        siteId: string;
        siteName: string;
    },
    organizationName: string;
    assetOwner: string;
    serialNumber: string;
    assetGroupId: number;
}


function capitalizeFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}


function AssetCard({ asset }: { asset: MotionAsset }) {
    let { url } = useRouteMatch();
    return (
        <Card>
            <CardHeader
                title={capitalizeFirstLetter(asset.assetName)}
                subheader={`${asset.site.siteName} - ${asset.organizationName}`}
            />
            <CardContent>
                {/*
                <Typography variant="body2" color="textSecondary" component="p">
                    {`Type: ${asset.assetType}`}
                </Typography>
                */}
                <Typography variant="body2" color="textSecondary" component="p">
                    {`Seriale: ${asset.serialNumber}`}
                </Typography>
                <Typography variant="body2" color="textSecondary" component="p">
                    {`Id: ${asset.motionAssetId}`}
                </Typography>
            </CardContent>
            <CardActions>
                <Link to={`${url}/asset/${asset.motionAssetId}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                    <Button size="small">Mostra Dati</Button>
                </Link>
            </CardActions>
        </Card>
    );
}

export default function SiteAssetsGrid() {
    const { token } = useAuthUser();
    let { siteId } = useParams<{ siteId: string }>();
    const { title, setTitle } = useContext(TitleContext);
    const { data, error } = useSWR(
        { url: `/api/abb/site/${siteId}/`, token: token },
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
    const assets = data?.assets;
    if (assets?.length === 0) {
        setTitle("");
        return <Typography sx={{ mt: 4, ml: 4 }}>Nessun asset per questo sito</Typography>;
    }
    const siteName = assets[0].site.siteName;
    setTitle(siteName);
    return (
        <Grid container spacing={3}>
            {assets.map((asset: MotionAsset) =>
                <Grid item xs={12} md={6} key={asset.motionAssetId}>
                    <AssetCard asset={asset} />
                </Grid>
            )}
        </Grid >
    );
}