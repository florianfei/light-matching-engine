package com.ff.model;

import java.util.Objects;

public class Pair {
    private final int price;
    private final Side side;

    public Pair(int price, Side side) {
        assert side == Side.B || side == Side.S;
        this.price = price;
        this.side = side;
    }

    public int getPrice() {
        return price;
    }

    public Side getSide() {
        return side;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Pair pair = (Pair) o;
        return price == pair.getPrice() && side == pair.getSide();
    }

    @Override
    public int hashCode() {
        return Objects.hash(price, side);
    }
}
