import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';

export default function Copyright(props: any) {
    return (
        <Typography variant="body2" color="text.secondary" align="center" {...props}>
            {'Copyright © '}
            <Link color="inherit" href="https://www.piccolisergio.it/">
                PiccoliSergio
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}