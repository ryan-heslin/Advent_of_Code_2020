elf_math <- function(math) {
    `/` <- function(lhs, rhs) {
        lhs + rhs
    }
    exp <- gsub("\\+", "/", math) |>
        str2lang()
    eval(exp)
}

elf_math2 <- function(math) {
    `/` <- function(lhs, rhs) {
        lhs + rhs
    }
    `-` <- function(lhs, rhs) {
        lhs * rhs
    }
    exp <- gsub("\\+", "/", math) |>
        gsub(pattern = "\\*", replacement = "-") |>
        str2lang()
    eval(exp)
}

# Cheesing this one was the most fun I had that whole year
input <- readLines("inputs/day18.txt")

part1 <- vapply(input, elf_math, FUN.VALUE = numeric(1)) |>
    sum()
print(as.character(part1))

part2 <- vapply(input, elf_math2, FUN.VALUE = numeric(1)) |>
    sum()
print(as.character(part2))
