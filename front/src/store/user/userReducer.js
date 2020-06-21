import {SET_USER, SET_TOKEN, SET_COMMUNITY} from "./userActionsTypes";
import axios from "axios";


const initState = {
    user: null,
    token: null,
    org_id: null,
    community: null
};


function userReducer(state = initState, action) {

    switch (action.type) {
        case SET_USER: {
            /*if(window.rg4js) {
                window.rg4js('getRaygunInstance').resetAnonymousUser();
                window.rg4js("setUser", {
                    identifier: action.user.id,
                    email: action.user.email,
                    isAnonymous: false,
                    fullName: action.user.first_name + " " + action.user.last_name,
                });
            }*/
            return Object.assign({}, {...state, user: action.user})
        }
        case SET_TOKEN: {
            console.log("SET TOKEN");
            console.log(axios.interceptors.request.handlers = []);
            axios.interceptors.request.use(
                config => {
                    if (action.token) {
                        config.headers['Authorization'] = 'Bearer ' + action.token
                    }
                    config.headers['Content-Type'] = 'application/json';
                    return config;
                },
                null);

            return Object.assign({}, {...state, token: action.token})
        }
        case SET_COMMUNITY: {
            return Object.assign({}, {...state, community: action.community})
        }
        default:
            return {...state};
    }
    return state
}

export default userReducer
