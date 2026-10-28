package com.hotel.model;

public class Booking {
    private int bookingId;
    private int gId;
    private int rId;
    private String bookingType;
    private String status;
    private String checkIn;
    private String checkOut;

    public Booking() {}
    public int getBookingId() { return bookingId; } public void setBookingId(int v) { this.bookingId = v; }
    public int getGId() { return gId; } public void setGId(int v) { this.gId = v; }
    public int getRId() { return rId; } public void setRId(int v) { this.rId = v; }
    public String getBookingType() { return bookingType; } public void setBookingType(String v) { this.bookingType = v; }
    public String getStatus() { return status; } public void setStatus(String v) { this.status = v; }
    public String getCheckIn() { return checkIn; } public void setCheckIn(String v) { this.checkIn = v; }
    public String getCheckOut() { return checkOut; } public void setCheckOut(String v) { this.checkOut = v; }
}
