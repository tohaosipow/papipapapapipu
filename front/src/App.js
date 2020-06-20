import React, {useState, useEffect} from 'react';
import bridge from '@vkontakte/vk-bridge';
import View from '@vkontakte/vkui/dist/components/View/View';
import ScreenSpinner from '@vkontakte/vkui/dist/components/ScreenSpinner/ScreenSpinner';
import '@vkontakte/vkui/dist/vkui.css';
import {useSelector, useDispatch} from "react-redux";
import Home from './panels/Home';
import Persik from './panels/Persik';
import Hello from "./panels/Hello";
import eruda from 'eruda'
import { createBrowserHistory } from 'history'

import {
    Switch,
    Route, HashRouter,
} from "react-router-dom";
import axios from "axios";
import {loadToken, loadUser} from "./store/user/userActions";
import GetCall from "./panels/Application/GetCall";
const history = createBrowserHistory();


const App = () => {


    const [load, setLoad] = useState(false);
    const [popout, setPopout] = useState(<ScreenSpinner size='large'/>);
    const currentUser = useSelector(state => state.user.user);


    const dispatch = useDispatch();


    useEffect(() => {



        bridge.send("VKWebAppInit", {});
        bridge.subscribe(({detail: {type, data}}) => {
            if (type === 'VKWebAppUpdateConfig') {
                const schemeAttribute = document.createAttribute('scheme');
                schemeAttribute.value = data.scheme ? data.scheme : 'client_light';
                document.body.attributes.setNamedItem(schemeAttribute);
            }
            if (type === 'VKWebAppViewRestore') {
                loadUser();
            }
        });

        dispatch(loadToken(window.location.search)).then(() => {
            dispatch(loadUser())
        });

        axios.interceptors.response.use(null, error => {
            if (!error.response) return Promise.reject(error);
            if (401 === error.response.status) {
                return dispatch(loadToken(window.location.search)).then(() => {
                    return axios.request(error.config);
                    /*return dispatch(loadUser()).then(() => {
                        return axios.request(error.config);
                    }) */
                });
            }
            return Promise.reject(error);
        });


    }, []);


    return (
        <HashRouter history={history}>
            <Switch>

                <Route path="/get_call/:group_id" component={GetCall}/>
                <Route path="/manage/:group_id" component={Hello}/>
                <Route path="/" component={Hello}/>
            </Switch>
        </HashRouter>
    );
}

export default App;

