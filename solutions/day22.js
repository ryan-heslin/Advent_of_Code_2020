const fs = require("fs");

function hash_game(players) {
    return players[0].toString() + "-" + players[1].toString();

}

function play(players, recurse) {
    let seen = new Set(hash_game(players))
    let init = true;
    let round_winner = null;
    while (players[0].length > 0 && players[1].length > 0) {
        let cards = [players[0].shift(), players[1].shift()];

        //No repeated states
        let this_hash = hash_game(players);
        if (seen.has(this_hash) && !(init)) {
            return [0, players[0]];
        }
        init = false
        seen.add(this_hash);

        if (recurse && players[0].length >= cards[0] && players[1].length >= cards[1]) {
            new_players = [null, null]
            new_players[0] = players[0].slice(0, cards[0])
            new_players[1] = players[1].slice(0, cards[1])
            round_winner = play(new_players)[0];
        } else {
            round_winner = Number(cards[1] > cards[0]);
        }
        if (round_winner == 0) {
            players[0].push(...cards);
        } else {
            cards.reverse()
            players[1].push(...cards);
        }
    }
    let winner = Number(players[1].length > 0);
    return [winner, players[winner]];
}

function score(cards) {
    cards.reverse();
    return (cards.map((x, i) => x * (i + 1))).reduce((x, y) => x + y);
}

const raw_input = fs.readFileSync('inputs/day22.txt', 'utf-8').toString()
    .replace(/\n+$/, "").replace(/Player.*\n/, "").replace(/Player.*\n/, "").split("\n\n");
const player1 = raw_input[0].split("\n").map(Number);
const player2 = raw_input[1].split("\n").map(Number);

const result1 = play([player1.slice(), player2.slice()], false);
const part1 = score(result1[1]);
console.log(part1);

const result2 = play([player1, player2], true);
const part2 = score(result2[1]);
console.log(part2);
