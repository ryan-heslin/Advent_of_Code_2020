const fs = require("fs");

// https://web.archive.org/web/20140418004051/http://dzone.com/snippets/calculate-all-combinations
var combo_sum = function(a) {
    var fn = function(n, src, got, all) {
        if (n == 0) {
            if (got.length > 0) {
                all[all.length] = got;
            }
            return;
        }
        for (var j = 0; j < src.length; j++) {
            fn(n - 1, src.slice(j + 1), got.concat([src[j]]), all);
        }
        return;
    }
    var all = [];
    for (var i = 0; i < a.length; i++) {
        fn(i, a, [], all);
    }
    all.push(a);
    return all;
}

function parse(line) {
    let parts = line.split(" = ")
    if (/mem/.test(parts[0])) {
        return [Number(/\[(\d+)\]/.exec(parts[0])[1]), Number(parts[1])];
    }
    return [parts[1]];
}

function solve_part1(lines) {

    let memory = {};
    let mask = null;
    for (line of lines) {
        //AND with mask complement (filling X with 1)
        // OR with pattern
        // New mask
        if (line.length == 1) {
            mask = line[0];
            mask = mask.split("").reverse()
            mask = mask.map((x) => x === "X" ? NaN : Number(x));
            complement = (~mask >>> 0) >>> 0;
        } else {
            let value = line[1];
            let result = 0;

            for (i = 0; i < 36; i++) {
                let is_one = (value % 2 != 0);
                value >>>= 1;
                result += (2 ** i) * (isNaN(mask[i]) ? is_one : mask[i])
                old_value = value;

            }
            memory[line[0]] = result;
        }
    }
    return Object.values(memory).reduce((x, y) => x + y);
}

function solve_part2(lines) {
    {
        let memory = {};
        let mask = null;
        for (line of lines) {
            if (line.length == 1) {
                mask = line[0].split("").reverse().map((x) => x === "X" ? NaN : Number(x));
            } else {
                let target = line[0];
                let value = line[1];
                let result = 0;
                let additions = [];

                for (i = 0; i < 36; i++) {
                    let is_one = (target % 2 != 0);
                    target >>>= 1;
                    power = 2 ** i;
                    let bit = mask[i];
                    if (bit == 1 || (bit == 0 && is_one)) {
                        result += power;
                    } else if (isNaN(bit)) {
                        additions.push(power)
                    }
                    old_target = target;
                }
                let summands = [[0]];
                if (additions.length > 0) {
                    summands = summands.concat(combo_sum(additions));
                }

                summands = summands.map((x) => x.reduce((y, z) => y + z))
                for (addition of summands) {
                    memory[result + addition] = value;
                }
            }
        }
        return Object.values(memory).reduce((x, y) => x + y);
    }
}

const raw_input = fs.readFileSync('inputs/day14.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n");
const parsed = raw_input.map(parse);

const part1 = solve_part1(parsed);
console.log(part1);

const part2 = solve_part2(parsed);
console.log(part2);
