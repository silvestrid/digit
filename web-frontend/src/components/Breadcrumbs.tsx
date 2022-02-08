import * as React from 'react';
import Typography from '@mui/material/Typography';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import { LocationOn, Sensors } from '@mui/icons-material';


function handleClick(event: React.MouseEvent<HTMLDivElement, MouseEvent>) {
    event.preventDefault();
}

export default function IconBreadcrumbs(props: { siteName: string, siteUrl: string, assetName: string }) {
    const { siteName, siteUrl, assetName } = props;
    if (!siteName)
        return <div></div>;
    let children = [
        <Link
            underline="hover"
            sx={{ display: 'flex', alignItems: 'center' }}
            color="inherit"
            href={siteUrl}
        >
            <LocationOn sx={{ mr: 0.5 }} fontSize="inherit" />
            {siteName}
        </Link>
    ];
    if (assetName) {
        children.push(
            <Typography
                sx={{ display: 'flex', alignItems: 'center' }}
                color="text.primary"
            >
                <Sensors sx={{ mr: 0.5 }} fontSize="inherit" />
                {assetName}
            </Typography>)
    }

    return (
        <div role="presentation" onClick={handleClick}>
            <Breadcrumbs aria-label="breadcrumb">
                {children}
            </Breadcrumbs>
        </div>
    );
}