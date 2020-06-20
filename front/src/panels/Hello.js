import React, {useEffect, useState} from 'react';
import PropTypes from 'prop-types';
import Panel from '@vkontakte/vkui/dist/components/Panel/Panel';
import PanelHeader from '@vkontakte/vkui/dist/components/PanelHeader/PanelHeader';
import Button from '@vkontakte/vkui/dist/components/Button/Button';
import Group from '@vkontakte/vkui/dist/components/Group/Group';
import Cell from '@vkontakte/vkui/dist/components/Cell/Cell';
import Div from '@vkontakte/vkui/dist/components/Div/Div';
import Avatar from '@vkontakte/vkui/dist/components/Avatar/Avatar';
import Placeholder from "@vkontakte/vkui/dist/components/Placeholder/Placeholder";
import Icon56MentionOutline from '@vkontakte/icons/dist/56/mention_outline';
import Icon56UsersOutline from '@vkontakte/icons/dist/56/users_outline';
import Icon28QrCodeOutline from '@vkontakte/icons/dist/28/qr_code_outline';
import Separator from "@vkontakte/vkui/dist/components/Separator/Separator";
import CardScroll from "@vkontakte/vkui/dist/components/CardScroll/CardScroll";
import Card from "@vkontakte/vkui/dist/components/Card/Card";
import Gallery from "@vkontakte/vkui/dist/components/Gallery/Gallery";
import Header from "@vkontakte/vkui/dist/components/Header/Header";
import Icon12OnlineVkmobile from '@vkontakte/icons/dist/12/online_vkmobile';
import Icon56GiftOutline from '@vkontakte/icons/dist/56/gift_outline';
import InfoRow from "@vkontakte/vkui/dist/components/InfoRow/InfoRow";
import Progress from "@vkontakte/vkui/dist/components/Progress/Progress";
import Icon56UserAddOutline from '@vkontakte/icons/dist/56/user_add_outline';
import bridge from '@vkontakte/vk-bridge';
import Icon24UserOutline from '@vkontakte/icons/dist/24/user_outline';
import {Route, useHistory} from "react-router-dom";
import View from "@vkontakte/vkui/dist/components/View/View";
import axios from 'axios';
import users from "../api/users";
import {useSelector} from "react-redux";
import {useDispatch} from "react-redux";
import Icon24Similar from '@vkontakte/icons/dist/24/similar';
    import Icon24Phone from '@vkontakte/icons/dist/24/phone';
import Icon24StorefrontOutline from '@vkontakte/icons/dist/24/storefront_outline';
import Icon28MoneyCircleOutline from '@vkontakte/icons/dist/28/money_circle_outline';
import {loadCommunity, setCommunity} from "../store/user/userActions";
import communities from "../api/communities";

const Hello = ({location}) => {
    const currentUser = useSelector(state => state.user.user);
    const currentToken = useSelector(state => state.user.token);
    const dispatch = useDispatch();

    const [activeSlide, setActiveSlide] = useState(0);

    const history = useHistory();
    const moveToNext = e => {
        setActiveSlide(activeSlide + 1);
    };

    useEffect(() => {

        let query = new URLSearchParams(window.location.search);
        let group_id = query.get('vk_group_id');
        let role = query.get('vk_viewer_group_role');
        if(group_id){
            dispatch(loadCommunity(group_id));
            history.push("get_call/"+group_id);
        }

    }, []);


    const goToApp = e => {
        history.push("/app");
    };


    const install = e => {
        bridge.send("VKWebAppAddToCommunity", {}).then((data) => {
            bridge.send("VKWebAppGetCommunityToken", {"app_id": 7516806, "group_id": data.group_id, "scope": "messages"}).then((r) => {
                const token = r.access_token;
                const id = data.group_id;
                communities.createCommunity(token, id).then((z) => {
                    dispatch(setCommunity(z.data));
                })
            });
        });
    };


    return (
        <View activePanel='hello'>
            <Panel id='hello'>
                <PanelHeader>Приветствие</PanelHeader>
                <Group>
                    <Group>
                        <Div>
                            <InfoRow title="Default">
                                <Progress value={(activeSlide + 1) / 5 * 100}/>
                            </InfoRow>
                        </Div>
                    </Group>
                    <Gallery
                        onDrag={() => setActiveSlide(2)}
                        slideWidth="100%"
                        slideIndex={activeSlide}
                        onChange={activeSlide => setActiveSlide(activeSlide)}
                        style={{height: 500}}
                    >
                        <Placeholder
                            icon={<Icon24Similar width={64} height={64}/>}
                            header="Сервис обратного звонка"
                            action={<Button onClick={moveToNext} size="l">Понятно</Button>}
                        >
                           Добро пожаловать! Сервис обратного звонка поможет Вам и вашим клиентам проще связываться.
                        </Placeholder>
                        <Placeholder
                            icon={<Icon12OnlineVkmobile width={64} height={64}/>}
                            header="Заказ звонка вашим клиентом"
                            action={<Button onClick={moveToNext} size="l">Понятно</Button>}
                        >
                            Добавляйте кнопку обратного звонка в ваше сообщество. Как только клиент закажет вызов, мы позвоним ему и вам и свяжем вас.
                        </Placeholder>
                        <Placeholder
                            icon={<Icon24Phone width={64} height={64}/>}
                            header="Получайте вызовы"
                            action={<Button onClick={moveToNext} size="l">Понятно</Button>}
                        >
                            Клиенты экономят на звонках вам, а вы получая звонок уже знаете все о клиенте: мы скажем как его зовут, из какого он города и другую информацию, которую вы выберите в настройках.
                        </Placeholder>
                        <Placeholder
                            icon={<Icon24StorefrontOutline width={64} height={64}/>}
                            header="Оставайтесь на связи"
                            action={<Button onClick={moveToNext} size="l">Удобное время звонка</Button>}
                        >
                           Клиент закажет обратный звонок и укажет, когда именно ему удобно позвонить, а мы сделаем это точно в срок. Вы в свою очередь укажите график работы своих менеджеров!
                        </Placeholder>
                        <Placeholder
                            icon={<Icon28MoneyCircleOutline width={64} height={64}/>}
                            header={"Начните прямо сейчас"}
                            action={<Button onClick={install} size="l">Начать</Button>}
                        >
                            Установите приложение в сообщество, настройте минимум параметров, начните принимать вызовы и зарабатывать!
                        </Placeholder>

                    </Gallery>
                </Group>

            </Panel>
        </View>
    )
};


export default Hello;
