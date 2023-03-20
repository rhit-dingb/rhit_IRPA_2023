import { TOKEN_KEY } from "../constants/constants"

export const checkResponse = (response, errorCallback, successCallback, history)=>{
    response.json().then(data=>{
        console.log(data)
        if(!response.ok) {
            
            if (response.status == 401) {
                console.log("SESSION EXPIRED")
                logOut(history)
                console.log(history)
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


export const logOut = (history)=>{
    localStorage.removeItem(TOKEN_KEY)
    // history.push('/');
}