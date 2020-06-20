export default {
    parseValue: (value) => {
        let ids = [];
        for (let i = 0; i <= Math.ceil(Math.log2(value)); i++) if (Math.pow(2, i) & value) ids.push(Math.pow(2, i));
        return ids;
    },

    toValue: (arr) => {
        return arr.reduce((a, b) => a + b)
    },

    in: (value, id) => {
        return (value & id) === id;
    }
}
