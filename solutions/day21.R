raw_input <- readLines("inputs/day21.txt")
allergens <- gsub(".*\\(contains ([^)]+)\\)", "\\1", raw_input) |>
    strsplit(",\\s+")
ingredients <- gsub("\\s\\(.*", "", raw_input) |>
    strsplit("\\s")

combined <- mapply(expand.grid,
    ingredient = ingredients,
    allergen = allergens, group = seq_along(allergens),
    stringsAsFactors = FALSE, SIMPLIFY = FALSE
) |>
    lapply(\(x) {
        x$contained <- length(unique(x$allergen))
        x
    }) |>
    do.call(what = rbind)

ingreds <- unique(input$ingred)
observed_groups <- tapply(combined$group, combined$allergen, unique)
combinations <- interaction(combined$ingredient, combined$allergen, drop = TRUE)

definite <- split(
    combined,
    f = combinations
)

definite <- definite[vapply(definite, \(x){
    setequal(
        x$group,
        observed_groups[[unique(x$allergen)]]
    )
}, FUN.VALUE = logical(1))] |>
    do.call(what = rbind) |>
    subset(subset = TRUE, select = c("ingredient", "allergen")) |>
    unique()

eliminations <- setdiff(unique(combined$ingredient), definite$ingredient)
part1 <- unique(combined[, c("group", "ingredient")]) |>
    subset(
        subset = ingredient %in% eliminations,
        select = "ingredient"
    ) |>
    nrow()
print(part1)

reduced <- definite
while (anyDuplicated(reduced$ingredient)) {
    counts <- table(reduced$ingredient)
    solved <- reduced[counts[reduced$ingredient] == 1, ]
    reduced <- rbind(reduced[!reduced$allergen %in% solved$allergen, ], solved)
}
part2 <-
    reduced[order(reduced$allergen), "ingredient"] |>
    paste(collapse = ", ")
print(part2)
