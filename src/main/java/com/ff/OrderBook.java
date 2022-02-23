package com.ff;

import com.ff.model.Order;
import com.ff.model.Pair;
import com.ff.model.Side;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.TreeMap;

public class OrderBook {
    private final TreeMap<Integer, List<Order>> buyOrders;
    private final TreeMap<Integer, List<Order>> sellOrders;
    private final HashMap<String, Pair> oidMapping;

    public OrderBook() {
        this.buyOrders = new TreeMap<>();
        this.sellOrders = new TreeMap<>();
        this.oidMapping = new HashMap<>();
    }

    public void addBuyOrder(Order order) {
        int key = order.getPrice();
        if (!buyOrders.containsKey(key)) {
            buyOrders.put(key, new LinkedList<>());
        }
        buyOrders.get(key).add(order);
        oidMapping.put(order.getOid(), new Pair(order.getPrice(), order.getSide()));
    }

    public void addSellOrder(Order order) {
        int key = order.getPrice();
        if (!sellOrders.containsKey(key)) {
            sellOrders.put(key, new LinkedList<>());
        }
        sellOrders.get(key).add(order);
        addOid(order.getOid(), order.getPrice(), order.getSide());
    }

    public void removeOrder(String oid) {
        if (!oidMapping.containsKey(oid)) {
            System.out.println("Unable to find an order for orderId: " + oid);
        } else {
            Pair priceSide = oidMapping.get(oid);
            if (priceSide.getSide() == Side.B) {
                buyOrders.get(priceSide.getPrice()).removeIf(order -> order.getOid().equals(oid));
                removeOid(oid);
            } else if (priceSide.getSide() == Side.S) {
                sellOrders.get(priceSide.getPrice()).removeIf(order -> order.getOid().equals(oid));
                removeOid(oid);
            }
        }
    }

    public void addOid(String oid, int price, Side side) {
        oidMapping.put(oid, new Pair(price, side));
    }

    public void removeOid(String oid) {
        oidMapping.remove(oid);
    }

    public TreeMap<Integer, List<Order>> getBuyOrders() {
        return buyOrders;
    }

    public TreeMap<Integer, List<Order>> getSellOrders() {
        return sellOrders;
    }

    public HashMap<String, Pair> getOidMapping() {
        return oidMapping;
    }
}
