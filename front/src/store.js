import {createStore, applyMiddleware, compose, combineReducers} from 'redux';
import {composeWithDevTools} from 'redux-devtools-extension';
import userReducer from "./store/user/userReducer";
import ReduxThunk from 'redux-thunk';


const rootReducer = combineReducers({
    user: userReducer
});


const store = createStore(rootReducer, {
    user: {
        user: null,
        token: null,
        org_id: null
    }
}, applyMiddleware(ReduxThunk));

const unsubscribe = store.subscribe(() => {
    window.rg4js('withCustomData', () => {
        const state = store.getState();
        return { state };
    });
    console.log(store.getState())
})
export default store;
