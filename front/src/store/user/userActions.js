import {SET_USER, SET_TOKEN, SET_COMMUNITY,} from "./userActionsTypes";
import users from "../../api/users";
import communities from "../../api/communities";

const loadUser = () => {
    return (dispatch, getState) => {
        return users.getUser().then((response) => {
            dispatch(setUser(response.data));
        });
    }

};

const loadCommunity = (community_vk_id) => {
    return (dispatch, getState) => {
        return communities.getCommunity(community_vk_id).then((r) => {
            dispatch(setCommunity(r.data));
        })
    }

};


const loadToken = (query) => {
    return (dispatch, getState) => {
        return users.getToken(query).then((response) => {
            localStorage.setItem('access_token', response.data.access_token);

            dispatch(setToken(response.data.access_token));

            return response.data.access_token;
        });
    }

};

const setUser = function (user) {
    return {
        type: SET_USER,
        user
    }
};

const setToken = function (token) {
    return {
        type: SET_TOKEN,
        token
    }
};


const setCommunity = function (community) {
    return {
        type: SET_COMMUNITY,
        community
    }
};


export {
    loadUser, setToken, loadToken, loadCommunity, setCommunity
}
