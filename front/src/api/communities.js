import endpoint from "./endpoint";
import axios from 'axios';

export default {

    getCommunity: (community_vk_id) => {
        return axios.get(endpoint + "/community/getCommunityByVkId/"+community_vk_id);
    },
    createCommunity: (api_key, community_vk_id) => {
        return axios.post(endpoint + "/community/create", {api_key, community_vk_id});
    },

}
