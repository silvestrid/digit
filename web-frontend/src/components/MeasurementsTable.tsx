import * as React from 'react';
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    /*
    [`&.${tableCellClasses.head}`]: {
        backgroundColor: theme.palette.common.black,
        color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
        fontSize: 14,
    },
    */
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    '&:last-child td, &:last-child th': {
        border: 0,
    },
}));

function createData(
    name: string,
    value?: number,
    minV?: number,
    maxV?: number,
) {
    return { name, value, minV, maxV };
}

const labels = {
    max_tot_time: 'H. Lavoro totali',
    sum_run_time: 'H. Lavoro nel mese',
    avg_acc_x: 'Acc. X - media',
    avg_acc_y: 'Acc. Y - media',
    avg_acc_z: 'Acc. Z - media',
    tvi: 'TVI',
    dvi: 'DVI'
}

const limits = {
    avg_acc_x: [0, 1.8],
    avg_acc_y: [0, 1.8],
    avg_acc_z: [0, 1.8],
    tvi: [0, 1.8],
}

type entry = {
    key: string,
    value: number
}

export default function CustomizedTables(props: any) {
    const { data } = props;
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 400 }} aria-label="customized table">
                <TableHead>
                    <TableRow>
                        <StyledTableCell></StyledTableCell>
                        <StyledTableCell align="right">Analisi</StyledTableCell>
                        <StyledTableCell align="right">Min</StyledTableCell>
                        <StyledTableCell align="right">Max</StyledTableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    <StyledTableRow key={0}>
                        <StyledTableCell component="th" scope="row">
                            {'H. Lavoro totali'}
                        </StyledTableCell>
                        <StyledTableCell align="right">{data['max_tot_time']?.toFixed(1)}</StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={1}>
                        <StyledTableCell component="th" scope="row">
                            {'H. Lavoro nel mese'}
                        </StyledTableCell>
                        <StyledTableCell align="right">{data['tot_run_time']?.toFixed(1)}</StyledTableCell>
                        <StyledTableCell align="right">0</StyledTableCell>
                        <StyledTableCell align="right">{24 * 31}</StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={100}>
                        <StyledTableCell component="th" scope="row">

                        </StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={2}>
                        <StyledTableCell component="th" scope="row">
                            {'Acc. X - media'}
                        </StyledTableCell>
                        <StyledTableCell align="right">{data['avg_acc_x']?.toFixed(3)}</StyledTableCell>
                        <StyledTableCell align="right">0</StyledTableCell>
                        <StyledTableCell align="right">1.8</StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={3}>
                        <StyledTableCell component="th" scope="row">
                            {'Acc. Y - media'}
                        </StyledTableCell>
                        <StyledTableCell align="right">{data['avg_acc_y']?.toFixed(3)}</StyledTableCell>
                        <StyledTableCell align="right">0</StyledTableCell>
                        <StyledTableCell align="right">1.8</StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={4}>
                        <StyledTableCell component="th" scope="row">
                            {'Acc. Z - media'}
                        </StyledTableCell>
                        <StyledTableCell align="right">{data['avg_acc_z']?.toFixed(3)}</StyledTableCell>
                        <StyledTableCell align="right">0</StyledTableCell>
                        <StyledTableCell align="right">1.8</StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={101}>
                        <StyledTableCell component="th" scope="row">

                        </StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={5}>
                        <StyledTableCell component="th" scope="row">
                            {'TVI'}
                        </StyledTableCell>
                        <StyledTableCell align="right">{data['tvi']?.toFixed(1)}</StyledTableCell>
                        <StyledTableCell align="right">0</StyledTableCell>
                        <StyledTableCell align="right">1.8</StyledTableCell>
                    </StyledTableRow>
                    <StyledTableRow key={6}>
                        <StyledTableCell component="th" scope="row">
                            {'DVI'}
                        </StyledTableCell>
                        <StyledTableCell align="right">{data['dvi']?.toFixed(1)}</StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                        <StyledTableCell align="right"></StyledTableCell>
                    </StyledTableRow>
                </TableBody>
            </Table>
        </TableContainer>
    );
}