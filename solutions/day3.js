const fs = require("fs");
function count_trees(slope) {
    let xmax = raw_input[0].length;
    let ymax = raw_input.length;
    let x = y = count = 0;

    while (y < ymax) {
        count += raw_input[y][x] == "#";
        x += slope[0];
        x %= xmax;
        y += slope[1];
    }
    return count;
}

const raw_input = fs.readFileSync('inputs/day3.txt', 'utf-8').toString().split("\n");
raw_input.pop();
const slopes = [[1, 1],
[3, 1],
[5, 1],
[7, 1],
[1, 2]];

const result = slopes.map(count_trees);
console.log(result[1])

const part2 = result.reduce((x, y) => x * y)
console.log(part2);
