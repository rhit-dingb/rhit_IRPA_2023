export const CUSTOM_BACKEND_API_STRING = process.env.NODE_ENV =="development"? "http://127.0.0.1:8000"  
: "http://irpa-chatbot.csse.rose-hulman.edu:8000"

export const RASA_API_STRING = process.env.NODE_ENV =="development"? "http://127.0.0.1:5005" 
: "http://irpa-chatbot.csse.rose-hulman.edu:5005"

console.log(CUSTOM_BACKEND_API_STRING)
console.log(RASA_API_STRING)


export const GET_AVAILABLE_YEARS_END_POINT = "/api/get_years_available"

export const DataType = {
	ANNUAL: "annual",
    DEFINITION: "definition"
}

export const RESPONSE_TYPE_KEY = "type"
export const CHATBOT_TEXT_MESSAGE_KEY = "text"
export const CHATBOT_IMAGE_MESSAGE_KEY = "image"
export const CHATBOT_CUSTOM_MESSAGE_KEY = "custom"
export const GET_AVAILABLE_OPTIONS_MESSAGE = "What can I ask you about?"

export const IS_LOGGED_IN_CONSTANT = "isLoggedIn"
export const TOKEN_KEY = "access_token"

export const ChatbotResponseType = {
	NORMAL_MESSAGE: "normal message",
	ACCORDION_LIST: "accordion list"
}



