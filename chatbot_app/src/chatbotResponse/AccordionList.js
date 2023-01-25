
import { ChatbotResponseType, RESPONSE_TYPE_KEY } from "../constants/constants"
import "../component/chatBot.css"
import React from "react";
import { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import ListSubheader from '@mui/material/ListSubheader';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import InboxIcon from '@mui/icons-material/MoveToInbox';

import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import StarBorder from '@mui/icons-material/StarBorder';

export function AccordionList() {
    
    const [expand, setExpand] = useState(false)

    return (
    <div className="msgalignstart">
        <BiBot className="botIcon" />
        <List
            className="botmsg"
            sx={{ width: '100%', maxWidth: 500}}
            component="nav"
            aria-labelledby="nested-list-subheader"
        >
            <h5>Here are a list of options you can ask me: </h5>
            <ListItemButton onClick={()=>{setExpand(!expand)}}>
                <ListItemIcon>
                <InboxIcon />
                </ListItemIcon>
                <ListItemText primary="Inbox" />
                {expand ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
            <Collapse in={expand} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                <ListItemButton sx={{ pl: 4 }}>
                    <ListItemIcon>
                    <StarBorder />
                    </ListItemIcon>
                    <ListItemText primary="Starred" />
                </ListItemButton>
                </List>
            </Collapse>
        </List>
    </div>)
}


