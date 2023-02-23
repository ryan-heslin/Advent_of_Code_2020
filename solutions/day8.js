const fs = require("fs");

function parse(line) {
    let parts = line.split(" ");
    return [parts[0], parseInt(parts[1])];
}

function solve_part1(instructions) {
    let acc = i = 0;
    let seen = new Set([])

    while (!(seen.has(i)) && i < instructions.length && i >= 0) {
        seen.add(i);
        if (instructions[i][0] == "jmp") {
            i += instructions[i][1];
        } else {
            if (instructions[i][0] == "acc") {
                acc += instructions[i][1];
            }
            i++;
        }
    }
    return [i, acc];
}

function solve_part2(instructions) {
    let swaps = { "jmp": "nop", "nop": "jmp" };
    const target = instructions.length
    for (let i = 0; i < target; i++) {
        let command = instructions[i][0];

        if (command in swaps) {
            instructions[i][0] = swaps[command];
            let result = solve_part1(instructions);
            if (result[0] == target) {
                return result[1];
            }
            instructions[i][0] = command;
        }
    }
    return null;
}

const raw_input = fs.readFileSync("inputs/day8.txt").toString().replace(/\n+$/, "").split("\n");
const instructions = raw_input.map(parse);
console.log(instructions)
const part1 = solve_part1(instructions);
console.log(part1[1]);

const part2 = solve_part2(instructions);
console.log(part2);
