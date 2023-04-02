import { Navbar } from "./Navbar";
import { Box, Card, List, Grid, InputLabel, MenuItem, Select, FormControl, ListItem, ListItemText, ButtonGroup, IconButton } from "@mui/material";
import { Bar, Pie } from "react-chartjs-2";
import { Chart, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from "chart.js";
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
    const [feedbackData, setFeedbackData] = useState({});
    const [intentData, setIntentData] = useState({});

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
    var columns = columnsListAll;

    const fetchGeneralStats = (apiParamStr) => {
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

    const fetchFeedbackStats = (apiParamStr) => {
        fetch('http://localhost:8000/feedback_stats/?' + apiParamStr)
            .then(res => res.json())
            .then(data => {
                setFeedbackData({
                    success_rate: data.success_rate,
                    successful_questions: data.successful_questions,
                    total_questions: data.total_questions
                });
            });
    }

    const fetchIntentStats = (apiParamStr) => {
        fetch('http://localhost:8000/intent_stats/?' + apiParamStr)
            .then(res => res.json())
            .then(data => {
                console.log(data);
            });
    }


    const handleChangeDisplayType = (event) => {
        setDisplayType(event.target.value);
        updateDisplay(event.target.value);
    }

    useEffect(() => {
        const current = new Date();
        const endDate = current.toISOString();
        const startDate = new Date(current.setMonth(current.getMonth() - 1)).toISOString();
        fetchGeneralStats('endDate='+endDate+'&startDate_short='+startDate);
        fetchFeedbackStats('endDate='+endDate+'&startDate='+startDate);
        fetchIntentStats('endDate='+endDate+'&startDate='+startDate);
    }, []);

    useEffect(() => {
        updateDisplay(displayType);
    }, [freqData, feedbackData, intentData, displayType]);

    const updateDisplay = (type) => {
        if(type == 0){
            Chart.unregister(ArcElement, Tooltip, Legend);
            Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);
            setDisplay(null);
        } else if(type == 1){
            Chart.unregister(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);
            Chart.register(ArcElement, Tooltip, Legend);
            setDisplay(null);
        } else if(type == 2){
            setDisplay(<DataGrid columns={columns} rows={freqData}/>);
        } else {
            setDisplay(null);
        }
    }

    const handleChangeRange = (event) => {
        setRange(event.target.value);
        const current = new Date();
        const end = current.toISOString();
        console.log(displayType);
        if(event.target.value == 0){
            const start = new Date(current.setMonth(current.getMonth() - 1)).toISOString();
            if(displayType == 0) {
                fetchIntentStats('endDate='+end+'&startDate='+start);
            } else if(displayType == 1) {
                fetchFeedbackStats('endDate='+end+'&startDate='+start);
            } else if(displayType == 2) {
                fetchGeneralStats('endDate='+end+'&startDate_short='+start);
            }
        } else if(event.target.value == 1){
            const start = new Date(current.setYear(current.getYear() - 1)).toISOString();
            if(displayType == 0) {
                fetchIntentStats('endDate='+end+'&startDate='+start);
            } else if(displayType == 1) {
                fetchFeedbackStats('endDate='+end+'&startDate='+start);
            } else if(displayType == 2) {
                fetchGeneralStats('endDate='+end+'&startDate_short='+start);
            }
        } else if(event.target.value == 2){
            const start = new Date(0).toISOString();
            if(displayType == 0) {
                fetchIntentStats('endDate='+end+'&startDate='+start);
            } else if(displayType == 1) {
                fetchFeedbackStats('endDate='+end+'&startDate='+start);
            } else if(displayType == 2) {
                fetchGeneralStats('endDate='+end);
            }
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
                                    <MenuItem value={0}>Intent Stats</MenuItem>
                                    <MenuItem value={1}>Feedback Stats</MenuItem>
                                    <MenuItem value={2}>List All</MenuItem>
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