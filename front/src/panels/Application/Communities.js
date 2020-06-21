import React from "react";
import {Panel, PanelHeader, Group, RichCell, Avatar, PanelHeaderButton} from "@vkontakte/vkui";
import {useSelector} from "react-redux";
import Icon28SettingsOutline from '@vkontakte/icons/dist/28/settings_outline';
import Icon24Add from '@vkontakte/icons/dist/24/add';
import {useHistory} from "react-router-dom";
import communities from "../../api/communities";
import {setCommunity} from "../../store/user/userActions";
import bridge from '@vkontakte/vk-bridge';
import {useDispatch} from "react-redux";


const Communities = (props) => {
    const currentUser = useSelector(state => state.user.user);
    const history = useHistory();
    const dispatch = useDispatch();


    const addApp = () => {
        bridge.send("VKWebAppAddToCommunity", {}).then((data) => {
            bridge.send("VKWebAppGetCommunityToken", {
                "app_id": 7516806,
                "group_id": parseInt(data.group_id),
                "scope": "messages"
            }).then((r) => {
                const token = r.access_token;
                const id = parseInt(data.group_id);
                communities.createCommunity(token, id).then((z) => {
                    dispatch(setCommunity(z.data));
                    history.push('/manage/' + z.data.community_vk_id);
                })
            });
        });
    };

    return <Panel id='hello'>
        <PanelHeader left={<PanelHeaderButton
            onClick={() => history.push('/publics')}><Icon24Add onClick={() => addApp()}/></PanelHeaderButton>} >Ваши сообщества</PanelHeader>
        <Group>
            {currentUser.admin_communities.map((c) => <RichCell onClick={() => {history.push('/manage/'+c.community_vk_id)}}
                disabled
                multiline
                before={<Avatar src={c.avatar_url} size={50}/>}
                caption={c.managers.length + " менеджер(а)"}
                after={<Icon28SettingsOutline/>}
            >
                {c.name}
            </RichCell>)
            }
        </Group>
    </Panel>
};

export default Communities;
