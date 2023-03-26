import { TOKEN_KEY } from "../constants/constants"
import {CUSTOM_BACKEND_API_STRING} from "../constants/constants"

export const checkResponse = (response, errorCallback, successCallback, history)=>{
    response.json().then(data=>{
        console.log(data)
        if(!response.ok) {
            
            if (response.status == 401) {
                console.log("SESSION EXPIRED")
                logOut(history)
                history.push({pathname:"/admin_login",  state: "Session expired, please log in again"})
            } else{
                errorCallback(JSON.stringify(data))
            }
          
        } else {
            console.log("RESPONSE NOT OKAY")
            console.log(response)
            
           successCallback(JSON.stringify(data))
        }
    })
   
}


export const getCurrentUser = (token, history, successCallback) => {
    return fetch(`${CUSTOM_BACKEND_API_STRING}/currentUser`, {
        method: 'GET',
        headers: {"Authorization": token}
    }).then((response) =>{
        checkResponse(response, (stringifyData)=>{}, 
        (stringifyData)=>{
            let userData = JSON.parse(stringifyData)
            successCallback(userData)
        }, history)
    })
}

export const logOut = (history)=>{
    localStorage.removeItem(TOKEN_KEY)
    // history.push('/');
}