const fs = require("fs");

function solve_part1(time, buses) {
    let waits = buses.map((x) => x - (time % x));
    let lowest = waits.indexOf(Math.min(...waits));
    return waits[lowest] * buses[lowest];
}


function create_congruence(x, i) {
    let modulus = Number(x);
    //Modulus is bus ID
    i %= modulus;
    //let remainder = modulus - i;
    return [i, modulus]
}

function search(congruences) {
    let current = congruences.shift()
    let remainder = current[0];
    let modulus = current[1];

    while (congruences.length > 0) {
        current = congruences.shift();
        let new_remainder = current[0];
        let new_modulus = current[1];
        let candidate = remainder;

        while (candidate % new_modulus != new_remainder) {
            candidate += modulus;
        }
        modulus *= new_modulus;
        remainder = candidate;
    }
    return [remainder, modulus];
}

const raw_input = fs.readFileSync('inputs/day13.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n");
const time = Number(raw_input[0]);
const buses = raw_input[1].replace(/(?:,x)+/g, "").split(",").map(Number);
const part1 = solve_part1(time, buses);
console.log(part1);

let congruences = raw_input[1].replace(/\n+$/).split(",").map(create_congruence).filter((x) => (!isNaN(x[1])));

let result = search(congruences.slice());
let remainder = result[0]
let modulus = result[1]
console.log(modulus - remainder);
