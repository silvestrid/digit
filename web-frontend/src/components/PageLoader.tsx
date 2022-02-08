import {
    Box, CircularProgress,
} from '@mui/material';

export default function PageLoader() {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%', height: '100%' }}>
            <CircularProgress />
        </Box>
    );
}