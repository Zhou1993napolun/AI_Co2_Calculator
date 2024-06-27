import '../assets/css/TableAndStatistic.css'
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
    [`&.${tableCellClasses.head}`]: {
        backgroundColor: theme.palette.common.black,
        color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
        fontSize: 14,
    },
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

function TableAndStatistic(props) {

    function createData(name, calories) {
        return { name, calories };
    }
    
    const rows = [
        createData('OS', props.os),
        createData('CPU', props.cpuname),
        createData('GPU', props.gpuname),
    ];

    return (
        <>
            <div className="tablecss">
                <div className='tablewenzi'>
                    <span>Hardware Platform Information</span>
                </div>
                <div>
                    <TableContainer component={Paper} sx={{ width: 670}}>
                        <Table sx={{ minWidth: 500}} aria-label="customized table">
                            <TableHead>
                                <TableRow>
                                    <StyledTableCell sx={{ width: 150}}>Component</StyledTableCell>
                                    <StyledTableCell align="left">Type</StyledTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {rows.map((row) => (
                                    <StyledTableRow key={row.name}>
                                        <StyledTableCell component="th" scope="row">
                                            <span style={{fontSize:"16px", fontWeight:700}}>
                                             {row.name}
                                          </span>
                                        </StyledTableCell>
                                        <StyledTableCell align="left" >
                                          <span style={{fontSize:"16px", fontWeight:700}}>
                                             {row.calories}
                                          </span>
                                        </StyledTableCell>
                                    </StyledTableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </div>
        </>
    );

}

export default TableAndStatistic;

