import { Navbar } from "./Navbar";
import { Box, Card, List, Grid, InputLabel, MenuItem, Select, FormControl, ListItem, ListItemText } from "@mui/material";
import { DataGrid } from '@mui/x-data-grid';
import { useState } from "react";

function Frequency() {
    const [range, setRange] = useState(0);
    const [freqData, setFreqData] = useState([]);

    const columns = [
        {
            field: 'id',
            headerName: 'ID',
            width: 220
        },
        {
            field: 'intent',
            headerName: 'Intent',
            width: 120
        },
        {
            field: 'question',
            headerName: 'Question Asked',
            width: 300
        },
        {
            field: 'time',
            headerName: 'Time Asked',
            width: 200,
        },
        {
            field: 'feedback',
            headerName: 'Feedback',
            width: 100
        }
    ];

    const handleChangeRange = (event) => {
        setRange(event.target.value);
        console.log(event.target.value);
        const current = new Date();
        const end = current.toISOString();
        if(event.target.value == 0){
            const start = new Date(current.setMonth(current.getMonth() - 1)).toISOString();
            fetchStats('endDate='+end+'&startDate_short='+start);
        } else if(event.target.value == 1){
            const start = new Date(current.setYear(current.getYear() - 1)).toISOString();
            fetchStats('endDate='+end+'&startDate_long='+start);
        } else if(event.target.value == 2){
            fetchStats('endDate='+end);
        }
    }

    const fetchStats = (apiParamStr) => {
        fetch('http://localhost:8000/general_stats/?' + apiParamStr)
            .then(res => res.json())
            .then(data => {
                setFreqData(data.map(entry => {
                    return {
                        id: entry._id.$oid,
                        intent: entry.intent,
                        question: entry.question_asked,
                        time: entry.time_asked.$date,
                        feedback: entry.user_feedback
                    };
                }));
            });
    }

    return (
        <div>
            <Navbar/>
            <Box sx={{ width: '90%', margin: "auto", marginTop:"3%"}}>
                <Grid container direction="column" justifyContent="flex-start" alignItems="stretch">
                    <Grid item>
                        <Box sx={{ width: '100%', margin: "auto"}}>
                            <FormControl>
                                <InputLabel id="time-range-label">Time Range</InputLabel>
                                <Select id="time-range" labelId="time-range-label" value={range} label="Time Range" onChange={handleChangeRange}>
                                    <MenuItem value={0}>Last Month</MenuItem>
                                    <MenuItem value={1}>Last Year</MenuItem>
                                    <MenuItem value={2}>All Time</MenuItem>
                                </Select>
                            </FormControl>
                        </Box>
                    </Grid>
                    <Grid item>
                        <Box sx={{ height: 520, width: '100%' }}>
                            <DataGrid columns={columns} rows={freqData}/>
                        </Box>
                    </Grid>
                </Grid>
            </Box>
        </div>
    )
}
export default Frequency