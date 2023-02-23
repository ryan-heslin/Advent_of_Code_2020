const fs = require("fs");

// Who would ever need to do silly operations like union or intersection on sets?
// Never change, JS standard library
function union(x, y) {
    return new Set([...x].concat([...y]));
}

function intersection(x, y) {
    let xs = [...x].filter((el) => y.has(el));
    let ys = [...y].filter((el) => x.has(el));
    return new Set(xs.concat(ys));
}

function solve(groups) {
    let part1 = part2 = 0;
    for (group of groups) {
        let parts = group.replace("\n+$", "").split("\n").map((x) => new Set(x.split("")));
        part1 += parts.reduce(union).size
        part2 += parts.reduce(intersection).size
    }
    return [part1, part2]
}



const raw_input = fs.readFileSync('inputs/day6.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n\n");

const result = solve(raw_input);
console.log(result[0]);
console.log(result[1]);
