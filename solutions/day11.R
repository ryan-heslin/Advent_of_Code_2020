find_nearest <- function(start, board, dx, dy, xmin, xmax, ymin, ymax, max_traverse = 1) {
    x <- start[[2]]
    y <- start[[1]]
    visited <- 0
    x <- x + dx
    y <- y + dy

    while (x >= xmin && x <= xmax && y >= ymin && y <= ymax && visited < max_traverse) {
        if (board[y, x] == 1) {
            return(c(y, x))
        }
        x <- x + dx
        y <- y + dy
        visited <- visited + 1
    }
    NULL
}

neighbor_getter <- function(board, max_traverse) {
    # rows are y, cols x
    lookup <- new.env()
    xmin <- ymin <- 1
    xmax <- ncol(board)
    ymax <- nrow(board)
    # starting from NW, going clockwise
    directions <- list(
        c(-1, -1), c(-1, 0), c(-1, 1), c(0, 1),
        c(1, 1), c(1, 0), c(1, -1), c(0, -1)
    )

    function(coord) {
        hash <- paste(coord, collapse = ",")
        value <- lookup[[hash]]
        if (!is.null(value)) {
            value
        }
        neighbors <- lapply(directions, function(pair) {
            find_nearest(
                coord, board, pair[[1]], pair[[2]],
                xmin, xmax, ymin, ymax,
                max_traverse
            )
        }) |>
            do.call(what = rbind)
        lookup[[hash]] <<- neighbors
        neighbors
    }
}

simulate <- function(board, neighbors, occupied_max = 3) {
    last_state <- matrix(0, nrow = nrow(board), ncol = ncol(board))
    #-1 for occupied
    while (!all(board == last_state)) {
        last_state <- board
        occupied <- which(board == -1, arr.ind = TRUE, useNames = FALSE) |>
            asplit(MARGIN = 1)

        unoccupied <- which(board == 1, arr.ind = TRUE, useNames = FALSE) |>
            asplit(MARGIN = 1)
        new_occupied <- vapply(unoccupied, \(x)
        sum(board[neighbors(x)] == -1) == 0, FUN.VALUE = logical(1))

        new_empty <- vapply(occupied, \(x)
        sum(board[neighbors(x)] == -1) > occupied_max, FUN.VALUE = logical(1))

        board[do.call(occupied[new_empty], what = rbind)] <- 1
        board[do.call(unoccupied[new_occupied], what = rbind)] <- -1
    }
    sum(board == -1)
}

raw_input <- readLines("inputs/day11.txt")

board <- gsub("L", "1", raw_input) |>
    gsub(pattern = "\\.", replacement = "0") |>
    strsplit("") |>
    do.call(what = rbind) |>
    as.matrix() |>
    `class<-`("integer")

current <- board

seats <- which(board == 1, arr.ind = TRUE) |>
    unname(force = TRUE) |>
    asplit(MARGIN = 1)
neighbors <- neighbor_getter(board, max_traverse = 1)
part1 <- simulate(current, neighbors)
print(part1)

neighbors <- neighbor_getter(board, max_traverse = Inf)
part2 <- simulate(board, neighbors, 4)
print(part2)
