const stats = {

    totalWin: 0,
    totalLose: 0,

    winStrike: 0,
    loseStrike: 0,

    lastPrediction: null
};

function updateStats(win){

    if(win){

        stats.totalWin++;
        stats.winStrike++;
        stats.loseStrike = 0;

    } else {

        stats.totalLose++;
        stats.loseStrike++;
        stats.winStrike = 0;
    }
}

module.exports = {
    stats,
    updateStats
};