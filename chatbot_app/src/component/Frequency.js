import { Navbar } from "./Navbar";
import { Box, Card, List, Grid, InputLabel, MenuItem, Select, FormControl, ListItem, ListItemText, ButtonGroup, IconButton } from "@mui/material";
import { Bar } from "react-chartjs-2";
import { DataGrid } from '@mui/x-data-grid';
import { useState, useEffect } from "react";

export const data = {
    test: true,

}

function Frequency() {
    /*
    range:
        0: last month
        1: last year
        2: all time
    */
    const [range, setRange] = useState(0);
    /*
    displayType:
        0: list by intent
        1: list by question
        2: list all
    */
    const [displayType, setDisplayType] = useState(0);
    const [display, setDisplay] = useState();

    const [freqData, setFreqData] = useState([]);

    const columnsListAll = [
        {
            field: 'question',
            headerName: 'Question Asked',
            width: 400
        },
        {
            field: 'intent',
            headerName: 'Intent',
            width: 120
        },
        {
            field: 'time',
            headerName: 'Time Asked',
            width: 200,
        },
        {
            field: 'feedback',
            headerName: 'Feedback',
            width: 200
        }
    ];
    const columnsListByIntent = [
        {
            field: 'intent',
            headerName: 'Intent',
            width: 200
        },
        {
            field: 'count',
            headerName: 'Count',
            width: 200
        }
    ];
    const columnsListByQuestion = [
        {
            field: 'question',
            headerName: 'Question',
            width: 400
        },
        {
            field: 'count',
            headerName: 'Count',
            width: 200
        }
    ];
    var columns = columnsListAll;

    const fetchStats = (apiParamStr) => {
        fetch('http://localhost:8000/general_stats/?' + apiParamStr)
            .then(res => res.json())
            .then(data => {
                setFreqData(data.map(entry => {
                    return {
                        id: entry._id.$oid,
                        question: entry.question_asked,
                        intent: entry.intent,
                        time: entry.time_asked.$date,
                        feedback: entry.user_feedback
                    };
                }));
            });
    }

    const testFreq = {
        id: 1,
        question: "test",
        intent: "test",
        time: new Date(),
        feedback: "test"
    }

    const handleChangeDisplayType = (event) => {
        setDisplayType(event.target.value);
        updateDisplay(event.target.value);
    }

    useEffect(() => {
        const current = new Date();
        fetchStats('endDate='+current.toISOString()+'&startDate_short='+new Date(current.setMonth(current.getMonth() - 1)).toISOString());
    }, []);

    useEffect(() => {
        updateDisplay(displayType);
    }, [freqData, displayType]);

    const updateDisplay = (type) => {
        if(type == 0){
            setDisplay(null);
        } else if(type == 1){
            console.log(freqData);
            setDisplay(<DataGrid columns={columns} rows={freqData}/>);
        } else {
            setDisplay(null);
        }
    }

    const handleChangeRange = (event) => {
        setRange(event.target.value);
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
        // updateDisplay(displayType);
    }

    return (
        <div>
            <Navbar/>
            <Box sx={{ width: '90%', margin: "auto", marginTop:"3%"}}>
                <Grid container direction="column" justifyContent="flex-start" alignItems="stretch">
                    <Grid item>
                        <Box sx={{ width: '100%', margin: "auto"}}>
                            <FormControl>
                                <InputLabel id="display-type-label">Display Type</InputLabel>
                                <Select id="display-type" labelId="display-type-label" value={displayType} label="Display Type" onChange={handleChangeDisplayType}>
                                    <MenuItem value={0}>List by Intent</MenuItem>
                                    <MenuItem value={1}>List All</MenuItem>
                                </Select>
                            </FormControl>
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
                        <Box sx={{ height: 520, width: '100%'}}>
                            {display}
                        </Box>
                    </Grid>
                </Grid>
            </Box>
        </div>
    )
}
export default Frequency