const axios = require("axios");
const logger = require("./logger");

async function fetchHistory() {

    try {

        const response = await axios.post(
            "https://ckygjf6r.com/api/webapi/GetNoaverageEmerdList",
            {
                pageSize: 20,
                pageNo: 1,
                typeId: 30,
                language: 0,
                random: Math.random().toString(36).substring(2),
                signature: "F79858BE17BB9AE547A8E551FBAB402A",
                timestamp: Math.floor(Date.now() / 1000)
            },
            {
                headers: {
                    "Content-Type": "application/json;charset=UTF-8",
                    "Authorization": `Bearer ${process.env.AUTH_TOKEN}`,
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://www.cklottery.top",
                    "Referer": "https://www.cklottery.top/"
                },
                timeout: 10000
            }
        );

        return response.data.data.list;

    } catch (err) {

        logger.error(err.message);
        return [];
    }
}

module.exports = fetchHistory;