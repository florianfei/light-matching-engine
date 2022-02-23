package com.ff.model;

import java.util.Date;

public class Trade {
    private Date time;
    private String sellId;
    private String buyId;
    private int quantity;
    private int price;

    public Trade(String sellId, String buyId, int quantity, int price, Date time) {
        this.sellId = sellId;
        this.buyId = buyId;
        this.quantity = quantity;
        this.price = price;
        this.time = time;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public String getSellId() {
        return sellId;
    }

    public void setSellId(String sellId) {
        this.sellId = sellId;
    }

    public String getBuyId() {
        return buyId;
    }

    public void setBuyId(String buyId) {
        this.buyId = buyId;
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
}
