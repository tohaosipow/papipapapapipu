import moment from "moment";
import gen_months from "./gen_months";

const smartDate = (date) => {
    return moment(date).format('D') + " " + gen_months.months[moment(date).format('M') - 1] + " " + moment(date).format('H:mm')
};


const smartDates = (start_at, end_at) => {
    const one_day = moment(start_at).diff(end_at, 'days') === 0;
    return smartDate(start_at) + " - " + smartDate(end_at);
};

export default {smartDate, smartDates}
