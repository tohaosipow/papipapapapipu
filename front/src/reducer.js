/*
import {LOAD_EVENTS, LOAD_USER, SET_ORG_ID, SET_TOKEN, SET_USER_POINTS, SET_VK_TOKEN, LOAD_USER_META} from './actionsTypes'


const initState = {
    user: null,
    token: null,
    org_id: null,
    events: []
};


function enrollApp(state = initState, action) {
    console.log(action.type);
    switch (action.type) {
        case LOAD_USER: {
            return Object.assign({}, {...state, user: action.user})
        }
        case SET_TOKEN: {
            return Object.assign({}, {...state, token: action.token})
        }
        case SET_ORG_ID: {
            return Object.assign({}, {...state, org_id: action.orgID})
        }
        case SET_USER_POINTS: {
            return Object.assign({}, {...state, user: {...state.user, points: action.points}})
        }
        case SET_VK_TOKEN: {
            return Object.assign({}, {...state, vk_token: action.token})
        }



        case LOAD_USER_META: {
            return Object.assign({}, {...state, user: {...state.user, meta: action.meta}})
        }

        default:
            return {...state};
    }
    return state
}

export default enrollApp
*/
