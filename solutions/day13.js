const fs = require("fs");
// https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
// Bezout coefficients
function bezout(a, b) {
    let old_r = a
    let r = b;
    let old_s = 1;
    let t = 1;
    let s = 0
    let old_t = 0;
    let tmp = NaN;

    while (r != 0) {
        let quotient = Math.floor(old_r / r);

        tmp = r;
        r = old_r - quotient * tmp;
        old_r = tmp;

        tmp = s;
        s = old_s - quotient * tmp;
        old_s = tmp;

        tmp = t;
        t = old_t - quotient * tmp;
        old_t = tmp;
    }
    return [old_s, old_t, old_r];


}

function reduce_congruences(congruences) {
    let current = congruences.shift();
    let remainder = current[0]
    let new_remainder = remainder;
    let modulus = current[1];
    let new_modulus = modulus;

    //FOr each two congruences:
    while (congruences.length > 0) {
        let current = congruences.shift();
        // Compute on two current moduli
        console.log("Congruence 1")
        console.log(remainder, modulus)
        console.log("Congruence 2")
        console.log(current[0], current[1])

        coefficients = bezout(modulus, current[1]);
        if (coefficients[0] * modulus + coefficients[1] * current != coefficients[2]) Error("Unequal")
        // Each is remainder-modulus pair
        console.log("Coefs:")
        console.log(coefficients)
        new_remainder = (current[0] * coefficients[0] * modulus) + (remainder * coefficients[1] * current[1]);
        new_modulus = modulus * current[1];
        new_remainder %= new_modulus;

        // If new_remainder < 0, increase by modulus to lowest positive integer
        if (new_remainder < 0) new_remainder += new_modulus * Math.ceil(Math.abs(new_remainder) / new_modulus);
        remainder = new_remainder;
        modulus = new_modulus;
        console.log(new_remainder, new_modulus)
        console.log("\n\n")
    }
    return [new_remainder, new_modulus];
    // modulus * = congruences[0][1];
    // Get Bezout coefficients of moduli
    // new_remainder =  sum of each multiplied by corresponding remainder
    // Return reduced modulus
}

// https://www.a-calculator.com/congruence/
function solve_congruence(remainder, modulus, multiple = 1) {
    let coefficients = bezout(multiple, modulus);
    return ((remainder * coefficients[0]) / coefficients[2]) % modulus;
    // console.log(result)
    // return modulus - result;

}

function solve_part1(time, buses) {
    let waits = buses.map((x) => x - (time % x));
    let lowest = waits.indexOf(Math.min(...waits));
    return waits[lowest] * buses[lowest];
}

function verify(congruences, solution) {
    return congruences.map((x) => (solution % x[1]) == x[0])
}

function create_congruence(x, i) {
    let modulus = Number(x);
    //Modulus is bus ID
    i %= modulus;
    //let remainder = modulus - i;
    console.log(i)
    console.log(modulus)
    //if (remainder < 0) remainder += modulus * (Math.ceil(Math.abs(remainder / modulus)));
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

console.log(raw_input[1].length)
let congruences = raw_input[1].replace(/\n+$/).split(",").map(create_congruence).filter((x) => (!isNaN(x[1])));
//let congruences = [[0, 3], [3, 4], [4, 5]];
console.log(congruences);
let reduced = reduce_congruences(congruences.slice());
reduced[0] %= reduced[1];
console.log(reduced);
const part2 = solve_congruence(...reduced);
console.log(part2);

//All prime, so we can use Chinese Remainder Theorem
//Must ignore id 0, since it has modulus 0, and test numbers evenly divisible by it
// Get congruences as index-value pairs from list
// Sort by modulus value, ignoring zero modulus
// Reduce into single congruence
// Find lowest solution of congruence greater than 100000000000000
//
//  modulus = congruences[0][1]
// While remaining pairs

const floor = 100000000000000;
let part3 = search(congruences.slice());
let remainder = part3[0]
let modulus = part3[1]
console.log(remainder)
console.log(modulus)
// if (remainder <= floor) {
//     remainder += modulus * Math.floor((floor - remainder) / modulus)
// }
console.log(modulus - remainder);
console.log(verify(congruences, modulus - remainder))
// candidate = remainder;
// remainder = candidate;
//
//
