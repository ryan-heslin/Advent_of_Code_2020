function between(low, high) {
    return function(x) {
        return low <= Number(x) && Number(x) <= high;
    }
}

function contains(values) {
    return function(x) {
        return (values.has(x));
    }
}

function height(x) {
    let parts = x.match(/^(\d{2,3})((?:cm)|(?:in))$/);
    if (parts == null || !(parts[1] && parts[2])) return false;

    let number = Number(parts[1]);
    return (parts[2] === "cm" && (150 <= number && number <= 193)) || (parts[2] === "in" && (59 <= number && number <= 76));
}

function matches(pattern) {
    return function(x) {
        return pattern.test(x);
    }
}


function solve(lines) {

    let part1 = part2 = 0;
    const eye_color = contains(new Set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]));
    const validators = {
        "byr": between(1920, 2002),
        "iyr": between(2010, 2020), "eyr": between(2020, 2030),
        "hgt": height, "hcl": matches(/#[0-9a-f]{6}/), "ecl": eye_color,
        "pid": matches(/^\d{9}$/)
    };
    let fields = Object.keys(validators);

    for (line of lines) {
        let has_fields = fields_valid = true;
        let parts = line.replace(/\n+$/, "").split(/\n|\s/);
        let mapping = Object.fromEntries(parts.map((x) => x.split(":")))

        for (field of fields) {
            if (!(field in mapping)) {
                has_fields = fields_valid = false;
                break
            }
            if (fields_valid && !(validators[field](mapping[field]))) {
                fields_valid = false;
            }
        }
        part1 += has_fields;
        part2 += fields_valid;
    }
    return [part1, part2]
}


const fs = require("fs");
const raw_input = fs.readFileSync('inputs/day4.txt', 'utf-8').toString().replace(/\n+$/, "").split("\n\n");

answer = solve(raw_input);
console.log(answer[0])
console.log(answer[1])
