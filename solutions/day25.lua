local step = function(value, subject_number, modulus)
    return (value * subject_number) % modulus
end

local crack = function(target, subject_number, modulus)
    local number = 1
    local value = 1

    while true do
        value = step(value, subject_number, modulus)
        if value == target then
            return number
        end
        number = number + 1
    end
end

local file = io.lines("inputs/day25.txt")
local lines = {}
for line in file do
    table.insert(lines, line)
end

local subject_number = 7
local modulus = 20201227
local card = tonumber(lines[1])
local door = tonumber(lines[2])

local card_loop = crack(card, subject_number, modulus)
local part1 = 1
for _ = 1, card_loop, 1 do
    part1 = step(part1, door, modulus)
end
print(part1)
