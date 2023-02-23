const fs = require("fs");
function replace(char, zero) {
    return char === zero ? "0" : "1";
}

function parse_numbers(line) {
    let row = parseInt([...line.substring(0, 7)].map((x) => replace(x, "F")).join(""), 2);
    let col = parseInt([...line.substring(7)].map((x) => replace(x, "L")).join(""), 2);
    return [row, col];
}

function seat_id(seat) {
    return (seat[0] * 8) + seat[1];
}

function find_id(ids) {
    let stop = ids.length - 1;
    for (let i = 0; i < stop; i++) {
        let part2 = seat_ids[i];
        if (seat_ids[i + 1] - part2 > 1) {
            return part2 + 1;
        }
    }
    return null;
}


const raw_input = fs.readFileSync('inputs/day5.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n");

const numbers = raw_input.map(parse_numbers);
console.log(numbers)
const seat_ids = numbers.map(seat_id);
const part1 = Math.max(...seat_ids);
console.log(part1);

seat_ids.sort();
console.log(seat_ids);
const part2 = find_id(seat_ids);
console.log(part2);

modulus = Math.prod(...buses)
