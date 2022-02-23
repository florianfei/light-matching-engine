package com.ff.model;

import java.util.Date;

public class Order {
    private String oid;
    private String stock;
    private Side side;
    private Date time;
    private int quantity;
    private int price;
    private final String type;

    // Standard limit order
    public Order(String oid, String stock, Side side, Date time, int quantity, int price, String type) {
        assert side == Side.S || side == Side.B;
        this.oid = oid;
        this.stock = stock;
        this.side = side;
        this.time = time;
        this.quantity = quantity;
        this.price = price;
        this.type = type;
    }

    // Standard market order
    public Order(String oid, String stock, Side side, Date time, int quantity, String type) {
        assert side == Side.S || side == Side.B;
        this.oid = oid;
        this.stock = stock;
        this.side = side;
        this.time = time;
        this.quantity = quantity;
        this.price = (side == Side.S) ? -1 : Integer.MAX_VALUE;
        this.type = type;
    }

    public String getOid() {
        return oid;
    }

    public void setOid(String oid) {
        this.oid = oid;
    }

    public String getStock() {
        return stock;
    }

    public void setStock(String stock) {
        this.stock = stock;
    }

    public Side getSide() {
        return side;
    }

    public void setSide(Side side) {
        this.side = side;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public int getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public String getType() {
        return type;
    }
}
