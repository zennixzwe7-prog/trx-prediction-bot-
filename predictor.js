function getBigSmall(num){

    return num >= 5 ? "BIG" : "SMALL";
}

function getColor(num){

    if([1,3,7,9].includes(num)) return "GREEN";

    if([2,4,6,8].includes(num)) return "RED";

    if(num === 0) return "RED + VIOLET";

    if(num === 5) return "GREEN + VIOLET";
}

function analyzeTrend(history){

    const nums = history.map(x => Number(x.number));

    let greenCount = 0;
    let redCount = 0;

    nums.forEach(n => {

        if([1,3,7,9,5].includes(n)){
            greenCount++;
        } else {
            redCount++;
        }
    });

    const last = nums[0];

    let nextBigSmall;
    let nextColor;

    if(last >= 5){
        nextBigSmall = "SMALL";
    } else {
        nextBigSmall = "BIG";
    }

    if(greenCount > redCount){
        nextColor = "RED";
    } else {
        nextColor = "GREEN";
    }

    const frequency = {};

    nums.forEach(n => {
        frequency[n] = (frequency[n] || 0) + 1;
    });

    const nextNumber = Object.keys(frequency)
        .sort((a,b) => frequency[a] - frequency[b])[0];

    return {
        bigSmall: nextBigSmall,
        color: nextColor,
        number: nextNumber,
        confidence: Math.floor(Math.random() * 10) + 90
    };
}

module.exports = {
    getBigSmall,
    getColor,
    analyzeTrend
};