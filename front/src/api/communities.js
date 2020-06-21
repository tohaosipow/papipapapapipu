import endpoint from "./endpoint";
import axios from 'axios';

export default {

    getCommunity: (community_vk_id) => {
        return axios.get(endpoint + "/community/getCommunityByVkId/" + community_vk_id);
    },
    createCommunity: (api_key, community_vk_id) => {
        return axios.post(endpoint + "/community/create", {api_key, community_vk_id});
    },

    addManager: (community_id, phone, name) => {
        return axios.put(endpoint + "/community/addManager/" + community_id,  {
                phone,
                name,
                is_blocked: false
            });
    },

    removeManager: (community_id, manager_id) => {
        return axios.put(endpoint + "/community/removeManager/" + community_id + "/managers/"+manager_id);
    },

    getCalls: (community_id) => {
        return axios.get(endpoint + "/calls/getCallHistory/" + community_id);
    },

    createCall: (community_id, client_phone, user_id, call_time, hidden) => {
        return axios.post(endpoint + "/calls/create_call/communities/" + community_id, {
            client_phone,
            user_id,
            call_time,
            hidden
        });
    },


}
