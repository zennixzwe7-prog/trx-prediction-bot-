require("dotenv").config();

const TelegramBot = require("node-telegram-bot-api");

const fetchHistory = require("./api");

const {
    getBigSmall,
    getColor,
    analyzeTrend
} = require("./predictor");

const {
    stats,
    updateStats
} = require("./stats");

const logger = require("./logger");

const bot = new TelegramBot(process.env.BOT_TOKEN, {
    polling: true
});

let lastPeriod = "";

async function runBot(){

    try {

        const history = await fetchHistory();

        if(!history.length) return;

        const current = history[0];

        if(current.issueNumber === lastPeriod){
            return;
        }

        if(stats.lastPrediction){

            const actualBigSmall =
                getBigSmall(Number(current.number));

            const actualColor =
                getColor(Number(current.number));

            const win =
                stats.lastPrediction.bigSmall === actualBigSmall ||
                stats.lastPrediction.color === actualColor;

            updateStats(win);
        }

        lastPeriod = current.issueNumber;

        const prediction = analyzeTrend(history);

        stats.lastPrediction = prediction;

        const message = `
╔══════════════╗
🚀 AI PREDICTION BOT
╚══════════════╝

📌 PERIOD
${current.issueNumber}

━━━━━━━━━━━━━━

🎯 BIG/SMALL
${prediction.bigSmall}

🎨 COLOUR
${prediction.color}

🔢 NUMBER
${prediction.number}

📊 CONFIDENCE
${prediction.confidence}%

━━━━━━━━━━━━━━

🏆 TOTAL WIN
${stats.totalWin}

❌ TOTAL LOSE
${stats.totalLose}

🔥 WIN STRIKE
${stats.winStrike}

💀 LOSE STRIKE
${stats.loseStrike}

━━━━━━━━━━━━━━

🤖 Railway AI System
`;

        await bot.sendMessage(
            process.env.CHAT_ID,
            message
        );

        logger.info(
            `Prediction Sent: ${current.issueNumber}`
        );

    } catch(err){

        logger.error(err.message);
    }
}

setInterval(runBot, 15000);

logger.info("Prediction Bot Started");