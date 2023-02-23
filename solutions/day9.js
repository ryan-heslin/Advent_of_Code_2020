const fs = require("fs");
function solve_part1(numbers, preamble_length = 25) {
    let sums = combo_sum(numbers.slice(0, preamble_length));
    for (let i = preamble_length; i < numbers.length; i++) {
        let num = numbers[i];
        let found = false;
        for (group of sums) {
            if ((group.has(num))) {
                found = true;
                break
            }
        }
        if (!found) {
            return num;
        }
        sums.shift();
        sums.push(new Set(numbers.slice(i - preamble_length + 1, i).map((x) => x + num)));
    }

}



function solve_part2(numbers, target) {

    let ranges = numbers.map((x) => [x]);
    ranges.pop();

    while (true) {
        let interval = 1;
        for (let i = 0; i < ranges.length; i++) {
            ranges[i].push(numbers[i + interval])
            if (ranges[i].reduce((x, y) => x + y) == target) {
                return ranges[i];
            }
        }
        numbers.shift();
        ranges.pop();
    }
}
function memo_sum(arr) {
    let record = {};
    return function(i, j) {
        let hash = i.toString() + "," + j.toString();
        if (hash in record) {
            return record[hash];
        }
        let result = arr[i] + arr[j];
        record[hash] = result;
        return result;
    }
}

function combo_sum(numbers) {
    let result = [];
    let summer = memo_sum(numbers);
    for (let i = 0; i < numbers.length; i++) {
        result[i] = new Set([]);
        for (let j = 0; j < numbers.length; j++) {
            if (j != i) {
                result[i].add(summer(i, j));
            }
        }

    }
    return result;
    //return numbers.map((x, i) => new Set(numbers.slice(i + 1).map((y) => x + y)));
}


const raw_input = fs.readFileSync('inputs/day9.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n");
const numbers = raw_input.map(Number);
const part1 = solve_part1(numbers, 25);
console.log(part1);

const result = solve_part2(numbers, part1)
console.log(Math.min(...result) + Math.max(...result));
