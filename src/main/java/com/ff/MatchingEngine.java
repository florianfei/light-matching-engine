package com.ff;

import com.ff.model.Order;
import com.ff.model.Side;
import com.ff.model.Trade;

import java.util.*;

public class MatchingEngine {
    private final HashMap<String, OrderBook> catalog;

    public MatchingEngine(String[] config) {
        catalog = new HashMap<>();
        for (String stock : config) {
            catalog.put(stock, new OrderBook());
        }
    }

    public List<Trade> process(Order order) {
        List<Trade> trades = new LinkedList<>();
        System.out.println("Processing order!");
        String stock = order.getStock();
        if (!catalog.containsKey(stock)) {
            System.out.println("Unable to find the given stock!");
            return new LinkedList<>();
        }
        OrderBook orderBook = catalog.get(stock);
        if (order.getSide() == Side.B) {
            trades = processBuyOrder(orderBook, order);
        } else if (order.getSide() == Side.S) {
            trades = processSellOrder(orderBook, order);
        }
        return trades;
    }

    public List<Trade> processBuyOrder(OrderBook orderBook, Order buyOrder) {
        List<Trade> trades = new LinkedList<>();
        SortedMap<Integer, List<Order>> sellOrders =  orderBook.getSellOrders().headMap(buyOrder.getPrice(), true);
        for (Map.Entry<Integer, List<Order>> sellOrdersByPrice : sellOrders.entrySet()) {
            while (buyOrder.getQuantity() == 0 || !sellOrdersByPrice.getValue().isEmpty()) {
                ListIterator<Order> listItr = sellOrdersByPrice.getValue().listIterator();
                while (listItr.hasNext()) {
                    Order sellOrder = listItr.next();
                    int minQuantity = Math.min(buyOrder.getQuantity(), sellOrder.getQuantity());
                    trades.add(new Trade(sellOrder.getOid(), buyOrder.getOid(), minQuantity, sellOrder.getPrice(), new Date()));
                    buyOrder.setQuantity(buyOrder.getQuantity() - minQuantity);
                    sellOrder.setQuantity(sellOrder.getQuantity() - minQuantity);
                    if (sellOrder.getQuantity() == 0) {
                        listItr.remove();
                        orderBook.removeOid(sellOrder.getOid());
                    }
                    if (buyOrder.getQuantity() == 0) {
                        break;
                    }
                }
            }
            if (buyOrder.getQuantity() == 0) {
                return trades;
            }
        }
        if (buyOrder.getQuantity() > 0) {
            orderBook.addBuyOrder(buyOrder);
        }
        return trades;
    }

    public List<Trade> processSellOrder(OrderBook orderBook, Order sellOrder) {
        List<Trade> trades = new LinkedList<>();
        SortedMap<Integer, List<Order>> buyOrders =  orderBook.getBuyOrders().headMap(sellOrder.getPrice(), true);
        for (Map.Entry<Integer, List<Order>> buyOrdersByPrice : buyOrders.entrySet()) {
            while (sellOrder.getQuantity() == 0 || !buyOrdersByPrice.getValue().isEmpty()) {
                ListIterator<Order> listItr = buyOrdersByPrice.getValue().listIterator();
                while (listItr.hasNext()) {
                    Order buyOrder = listItr.next();
                    int minQuantity = Math.min(sellOrder.getQuantity(), buyOrder.getQuantity());
                    trades.add(new Trade(sellOrder.getOid(), buyOrder.getOid(), minQuantity, buyOrder.getPrice(), new Date()));
                    sellOrder.setQuantity(sellOrder.getQuantity() - minQuantity);
                    buyOrder.setQuantity(buyOrder.getQuantity() - minQuantity);
                    if (buyOrder.getQuantity() == 0) {
                        listItr.remove();
                        orderBook.removeOid(sellOrder.getOid());
                    }
                    if (sellOrder.getQuantity() == 0) {
                        break;
                    }
                }
            }
            if (sellOrder.getQuantity() == 0) {
                return trades;
            }
        }
        if (sellOrder.getQuantity() > 0) {
            orderBook.addSellOrder(sellOrder);
        }
        return trades;
    }

    public List<Trade> processIcebergsSellOrder(OrderBook orderBook, Order sellOrder) {
        List<Trade> trades = new LinkedList<>();
        SortedMap<Integer, List<Order>> buyOrders =  orderBook.getBuyOrders().headMap(sellOrder.getPrice(), true);
        for (Map.Entry<Integer, List<Order>> buyOrdersByPrice : buyOrders.entrySet()) {
            while (sellOrder.getQuantity() == 0 || !buyOrdersByPrice.getValue().isEmpty()) {
                LinkedList<Order> reinsertedOrders = new LinkedList<>();
                ListIterator<Order> listItr = buyOrdersByPrice.getValue().listIterator();
                while (listItr.hasNext()) {
                    Order buyOrder = listItr.next();
                    // TODO: USE DISPLAY SIZE
                    int minQuantity = Math.min(sellOrder.getQuantity(), buyOrder.getQuantity());
                    trades.add(new Trade(sellOrder.getOid(), buyOrder.getOid(), minQuantity, buyOrder.getPrice(), new Date()));
                    sellOrder.setQuantity(sellOrder.getQuantity() - minQuantity);
                    buyOrder.setQuantity(buyOrder.getQuantity() - minQuantity);
                    if (buyOrder.getQuantity() == 0) {
                        listItr.remove();
                        reinsertedOrders.add(buyOrder);
                    }
                    if (sellOrder.getQuantity() == 0) {
                        break;
                    }
                }
                buyOrdersByPrice.getValue().addAll(reinsertedOrders);
            }
            if (sellOrder.getQuantity() == 0) {
                return trades;
            }
        }
        if (sellOrder.getQuantity() > 0) {
            orderBook.addSellOrder(sellOrder);
        }
        return trades;
    }

    public HashMap<String, OrderBook> getCatalog() {
        return catalog;
    }
}
