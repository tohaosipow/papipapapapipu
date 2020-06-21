import React, {useEffect, useState} from "react";

import Icon24Phone from '@vkontakte/icons/dist/24/phone';
import {loadCommunity} from "../../store/user/userActions";
import {useSelector, useDispatch} from "react-redux";

import "imrc-datetime-picker/dist/imrc-datetime-picker.css";
import {DatetimePickerTrigger} from 'imrc-datetime-picker';
import moment from 'moment-jalaali';
import bridge from '@vkontakte/vk-bridge';
import {PanelHeader, Panel, Input, Spinner, SelectMimicry, Div, Checkbox, Button, Placeholder, FormLayout, PanelHeaderButton, View} from "@vkontakte/vkui";
import Icon28SettingsOutline from '@vkontakte/icons/dist/28/settings_outline';
import {useHistory} from "react-router-dom";
import communities from "../../api/communities";



const GetCall = (props) => {

    const dispatch = useDispatch();

    const [phone, setPhone] = useState("");
    const [call, setCall] = useState(0);
    const [date, setDate] = useState(moment());
    const [role, setRole] = useState(null);
    const [responsePhone, setResponsePhone] = useState(false);
    const community = useSelector(state => state.user.community);
    const currentUser = useSelector(state => state.user.user);

    const getPhone = () => {
        if(!responsePhone) {
            bridge.send("VKWebAppGetPhoneNumber", {}).then((data) => {
                setPhone("+" + data.phone_number);
                setResponsePhone(true);
            })
        }
    };

    const makeCall = () => {
        communities.createCall(community.id, phone, currentUser.id, date.format(), false);
        setCall(2);
    };

    const history = useHistory();

    useEffect(() => {
        let query = new URLSearchParams(window.location.search);
        let group_id = query.get('vk_group_id');
        setRole(query.get('vk_viewer_group_role'));
        let gr2 = props.match.params.group_id;
        if (group_id || gr2) {
            dispatch(loadCommunity(gr2));
        }
        else history.push("/");
    }, []);

    const defaultMoment = moment();


    return community ? <View activePanel='hello'>
        <Panel id='hello'>
            <PanelHeader  left={role === 'admin' && <PanelHeaderButton onClick={() => {history.push("/manage/"+community.community_vk_id)}}><Icon28SettingsOutline/></PanelHeaderButton>}>Заказ звонка</PanelHeader>

            {call === 2?<div>
                    <Placeholder
                        icon={ <Spinner size="large" />}
                        header="Мы уже звоним Вам"
                        action={<Button onClick={() => {bridge.send("VKWebAppClose", {"status": "success"});}}>Спасибо</Button>}
                    >
                        Скоро вы получите звонок от {community.name}
                    </Placeholder>

                </div>
            :<div>
                    <Placeholder
                        icon={<Icon24Phone width={64} height={64}/>}
                        header="Мы Вам перезвоним"
                    >
                        Вы собираетесь заказать звонок от {community.name}
                    </Placeholder>
                    <FormLayout>

                        <Input   bottom={phone && phone.match(/\+7\d{10}/g) ? '' : 'Пожалуйста, введите телефон в международном формате'}   status={phone.match(/\+7\d{10}/g) ? 'valid' : 'error'} value={phone} onChange={(e) => {
                            setPhone(e.target.value)
                        }} onClick={() => getPhone()} top={"Номер телефона"} type="text" placeholder="+7 912 345 67 89"/>

                        <Input type={"datetime-local"} valid={date.length > 2?"valid":"error"} min={moment().format("YYYY-MM-DDTHH:mm")} value={moment(date).format("YYYY-MM-DDTHH:mm")}  onChange={(e) => {setDate(moment(e.target.value))
                        }}  top={"Дата и время для звонка"} placeholder="+7 912 345 67 89"/>



                        <Checkbox> <b>Не передавать</b> мой номер менеджерам сообщества</Checkbox>
                    </FormLayout>
                    <Div>
                        <Button disabled={phone.match(/\+7\d{10}/g) === null} onClick={() => makeCall()} size={"xl"}>Заказать звонок</Button>
                    </Div>
                </div>
            }
        </Panel>
    </View> : ""
};
export default GetCall;
