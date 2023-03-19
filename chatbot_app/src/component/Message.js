import React from "react";
import { react, useEffect, useState, useRef } from "react";
import { checkResponse } from "../functions/functions";
function Message({response, successCallback, failedCallback, history}) {
    const [showMessage, setShowMessage] = useState(false)
    const [severity, setSeverity] = useState("error")

    const successFunctionWrapper = (stringifiedJsonResponse)=>{
        setShowMessage(true)
        successCallback()
    }

    const failedFunctionWrapper = (stringifiedJsonResponse)=>{
        setShowMessage(true)
        failedCallback()
    }


    useEffect(() => {
        checkResponse(response, successFunctionWrapper, failedFunctionWrapper, history)
    }, [])

    
}