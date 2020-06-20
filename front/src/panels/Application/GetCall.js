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
import "imrc-datetime-picker/dist/imrc-datetime-picker.css";
import {DatetimePickerTrigger} from 'imrc-datetime-picker';
import moment, {months} from 'moment-jalaali';
import PanelSpinner from "@vkontakte/vkui/dist/components/PanelSpinner/PanelSpinner";
import Spinner from "@vkontakte/vkui/dist/components/Spinner/Spinner";
import {SelectMimicry} from "@vkontakte/vkui";

const GetCall = () => {

    const dispatch = useDispatch();

    const [phone, setPhone] = useState("");
    const [call, setCall] = useState(0);
    const [date, setDate] = useState(moment());
    const community = useSelector(state => state.user.community);

    const getPhone = () => {
        bridge.send("VKWebAppGetPhoneNumber", {}).then((data) => {
            setPhone("+"+data.phone_number);
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

    const defaultMoment = moment();

    return community ? <View activePanel='hello'>
        <Panel id='hello'>
            <PanelHeader>Заказ звонка</PanelHeader>

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
                        <Input value={phone} onChange={(e) => {
                            setPhone(e.target.value)
                        }} onClick={() => getPhone()} top={"Номер телефона"} type="text" placeholder="+7 912 345 67 89"/>


                        <DatetimePickerTrigger
                            width={"100%"}
                            onChange={(e) => {
                                setDate(e)
                            }}
                            minDate={moment()}
                            position={"top"}
                            showTimePicker={true}
                            moment={date}
                            lang={"ru"}
                        >
                            <FormLayout>
                                <SelectMimicry top={"Дата и время звонка"} placeholder={date && date.format("DD.MM HH:mm")} type="text"/>
                            </FormLayout>
                        </DatetimePickerTrigger>

                        <Checkbox> <b>Не передавать</b> мой номер менеджерам сообщества</Checkbox>
                    </FormLayout>
                    <Div>
                        <Button onClick={() => setCall(2)} size={"xl"}>Заказать звонок</Button>
                    </Div>
                </div>
            }
        </Panel>
        <Panel id="countries">
            <PanelHeader>
                Выберите время звонка
            </PanelHeader>
            <Group>
            </Group>
        </Panel>
    </View> : ""
};
export default GetCall;
