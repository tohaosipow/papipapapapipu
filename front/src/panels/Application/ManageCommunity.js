import React, {useEffect, useState} from "react";
import {
    PanelHeader,
    Panel,
    PanelHeaderButton,
    RichCell,
    Avatar,
    Header,
    Tabs,
    TabsItem,
    Group,
    SimpleCell,
    Separator, List, View,
    ModalPage, ModalRoot, ModalPageHeader,
    HorizontalScroll,
    FormLayout, FormLayoutGroup, Input, Button, Div, CellButton, PanelHeaderContent, Placeholder
} from "@vkontakte/vkui";
import Icon28SettingsOutline from '@vkontakte/icons/dist/28/settings_outline';
import {useDispatch, useSelector} from "react-redux";
import {loadCommunity} from "../../store/user/userActions";
import {useHistory} from "react-router-dom";
import communities from "../../api/communities";
import Icon28DeleteOutline from '@vkontakte/icons/dist/28/delete_outline';
import Icon24BrowserBack from '@vkontakte/icons/dist/24/browser_back';
import Icon20PhoneOutline from '@vkontakte/icons/dist/20/phone_outline';
import Icon28UserAddOutline from '@vkontakte/icons/dist/28/user_add_outline';
import Gallery from "@vkontakte/vkui/dist/components/Gallery/Gallery";
import moment from "moment";

const ManageCommunity = (props) => {

    const dispatch = useDispatch();
    const history = useHistory();
    const community = useSelector(state => state.user.community);

    const [activeModal, setActiveModal] = useState(null);
    const [activeTab, setActiveTab] = useState('managers');
    const [calls, setCalls] = useState('managers');
    const [managerName, setManagerName] = useState("");
    const [managerPhone, setManagerPhone] = useState("");


    const removeManager = (manager_id) => {
        communities.removeManager(community.id, manager_id).then((r) => {
            dispatch(loadCommunity(community.community_vk_id));
        });
    };

    useEffect(() => {
        let query = new URLSearchParams(window.location.search);
        let group_id = query.get('vk_group_id');
        let gr2 = props.match.params.group_id;
        if (group_id || gr2) {
            dispatch(loadCommunity(props.match.params.group_id));
        } else history.push("/");
    }, []);

    useEffect(() => {
        if (community) communities.getCalls(community.id).then((r) => {
            setCalls(r.data);
        })

    }, [community]);


    const saveManager = () => {
        communities.addManager(community.id, managerPhone, managerName).then((r) => {
            dispatch(loadCommunity(community.community_vk_id));
            setActiveModal(null);
        });
    };

    const modal = (
        <ModalRoot
            activeModal={activeModal}
            onClose={() => {
                setActiveModal(null)
            }}
        >
            <ModalPage onClose={() => {
                setActiveModal(null)
            }} id={'addManager'} header={<ModalPageHeader>Добавление менеджера</ModalPageHeader>}>
                <FormLayout>
                    <Input onChange={(e) => setManagerName(e.target.value)} top={"Имя"} placeholder="Иван"/>
                    <Input onChange={(e) => setManagerPhone(e.target.value)} top={"Телефон"}
                           placeholder="+7 912 345 67 89"/>
                    <Button onClick={() => saveManager()} size={"xl"}>Добавить</Button>
                </FormLayout>
            </ModalPage>
        </ModalRoot>
    );


    return community ? <View modal={modal} activePanel={'hello'}><Panel id='hello'>
        <PanelHeader left={<PanelHeaderButton
            onClick={() => history.push('/publics')}>
            <Icon24BrowserBack/>
        </PanelHeaderButton>}>

            <PanelHeaderContent
                status={community.managers.length + " менеджер(а)"}
                before={<Avatar size={36} src={community.avatar_url}/>}
            >
                Сообщество {community.name}
            </PanelHeaderContent>

        </PanelHeader>

        <Tabs mode={"buttons"}>
            <HorizontalScroll>
                <TabsItem onClick={() => history.push("/get_call/"+community.community_vk_id)}
                          selected={activeTab === 'test'}
                >
                    Заказ звонка
                </TabsItem>
            <TabsItem onClick={() => setActiveTab('managers')}
                      selected={activeTab === 'managers'}
            >
                Список менеджеров
            </TabsItem>
            <TabsItem onClick={() => setActiveTab('calls')}
                      selected={activeTab === 'calls'}
            >
                Вызовы
            </TabsItem>

            </HorizontalScroll>
        </Tabs>
        {activeTab === 'managers' && <div>
            <Header>Менеджеры</Header>
            {community.managers.length === 0 ? <Placeholder
                icon={<Icon28UserAddOutline width={64} height={64}/>}
                header="Сервис обратного звонка"
                action={<Button onClick={() => {
                    setActiveModal('addManager')
                }} size="l">Добавить</Button>}
            >
                Добавьте менеджеров, с которым могли бы связаться клиенты.
            </Placeholder> : <Group>
                <CellButton onClick={() => {
                    setActiveModal('addManager')
                }} before={<Icon28UserAddOutline height={22} width={22}/>}>Добавить менеджера</CellButton>
            </Group>}

            {community.managers.map((man) => {
                return <SimpleCell description={man.phone}
                                   after={<Icon28DeleteOutline height={22} width={22} fill={"red"} onClick={() => {
                                       removeManager(man.id)
                                   }}/>}>{man.name}</SimpleCell>
            })} </div>}


        {activeTab === 'calls' &&
        <div>
            <Header>Вызовы</Header>
            {calls.length === 0 && <Placeholder
                icon={<Icon20PhoneOutline width={64} height={64}/>}
                header="Вызовы"
            >
               Здесь будут звонки ваших менеджеров. Как только кто-то закажет звонок.
            </Placeholder>}
            <List>
                {calls.map((call) => {
                    return <RichCell caption={moment(call.call_time).format("DD.MM HH:ss")}
                                     before={<Avatar src={call.client_avatar}/>}
                                     text={"Менеджер: " + call.manager_name}>{call.client_name}</RichCell>
                })}
            </List>
        </div>
        }


    </Panel></View> : "";
};

export default ManageCommunity;
