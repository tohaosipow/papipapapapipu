import endpoint from "./endpoint";
import axios from 'axios';

export default {
    getToken: (query) => {
        return axios.post(endpoint + "/users/authByVk" + query);
    },
    getUser: () => {
        return axios.get(endpoint + "/users/")
    },


}
