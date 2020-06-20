import endpoint from "./endpoint";
import axios from 'axios';

export default {

    getCommunity: (community_vk_id) => {
        return axios.get(endpoint + "/community/getCommunityByVkId/"+community_vk_id);
    },


}
