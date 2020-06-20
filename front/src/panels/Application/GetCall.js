import React, {useEffect, useState} from "react";
import View from "@vkontakte/vkui/dist/components/View/View";
import Panel from "@vkontakte/vkui/dist/components/Panel/Panel";
import PanelHeader from "@vkontakte/vkui/dist/components/PanelHeader/PanelHeader";
import Group from "@vkontakte/vkui/dist/components/Group/Group";
import FormLayoutGroup from "@vkontakte/vkui/dist/components/FormLayoutGroup/FormLayoutGroup";
import Input from "@vkontakte/vkui/dist/components/Input/Input";
import FormLayout from "@vkontakte/vkui/dist/components/FormLayout/FormLayout";
import Select from "@vkontakte/vkui/dist/components/Select/Select";
import Placeholder from "@vkontakte/vkui/dist/components/Placeholder/Placeholder";
import Button from "@vkontakte/vkui/dist/components/Button/Button";
import Gallery from "@vkontakte/vkui/dist/components/Gallery/Gallery";
import Icon24Phone from '@vkontakte/icons/dist/24/phone';
import Checkbox from "@vkontakte/vkui/dist/components/Checkbox/Checkbox";
import Div from "@vkontakte/vkui/dist/components/Div/Div";
import bridge from '@vkontakte/vk-bridge';
import {loadCommunity} from "../../store/user/userActions";
import {useSelector, useDispatch} from "react-redux";

const GetCall = () => {

    const dispatch = useDispatch();

    const [phone, setPhone] = useState(null);
    const [call, setCall] = useState(null);
    const community = useSelector(state => state.user.community);

    const getPhone = () => {
        bridge.send("VKWebAppGetPhoneNumber", {}).then((data) => {
            setPhone(data.phone_number);
        })
    };


    useEffect(() => {
        let query = new URLSearchParams(window.location.search);
        let group_id = query.get('vk_group_id');
        let role = query.get('vk_viewer_group_role');
        if (group_id) {
            dispatch(loadCommunity(group_id));
        }
    }, []);

    return community?<View activePanel='hello'>
        <Panel id='hello'>
            <PanelHeader>Заказ звонка</PanelHeader>
            <Placeholder
                icon={<Icon24Phone width={64} height={64}/>}
                header="Мы Вам перезвоним"
            >
                Вы собираетесь заказать звонок от {community.name}
            </Placeholder>
            <FormLayout>
                <Input value={phone} onChange={(e) => {
                    setPhone(e.target.value)
                }} onClick={() => getPhone()} top={"Номер телефона"} type="text" placeholder="+7 912 345 67 89"/>
                <Select value={"m"} top={"Удобное время для звонка"} placeholder="Укажите время">
                    <option value="m">Прямо сейчас</option>
                </Select>
                <Checkbox> <b>Не передавать</b> мой номер менеджерам сообщества</Checkbox>
            </FormLayout>
            <Div>
                <Button size={"xl"}>Заказать звонок</Button>
            </Div>
        </Panel>
    </View>:""
};
export default GetCall;
