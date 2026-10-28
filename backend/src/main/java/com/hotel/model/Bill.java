package com.hotel.model;

public class Bill {
    private int bId;
    private int gId;
    private double amount;
    private String billingDate;
    private String paymentStatus;
    private Integer bookingId;

    public Bill() {}
    public int getBId() { return bId; } public void setBId(int v) { this.bId = v; }
    public int getGId() { return gId; } public void setGId(int v) { this.gId = v; }
    public double getAmount() { return amount; } public void setAmount(double v) { this.amount = v; }
    public String getBillingDate() { return billingDate; } public void setBillingDate(String v) { this.billingDate = v; }
    public String getPaymentStatus() { return paymentStatus; } public void setPaymentStatus(String v) { this.paymentStatus = v; }
    public Integer getBookingId() { return bookingId; } public void setBookingId(Integer v) { this.bookingId = v; }
}
