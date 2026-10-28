package com.hotel.model;

public class Room {
    private int rId;
    private String type;
    private int capacity;
    private String availability;
    private double pricePerNight;

    public Room() {}
    public Room(int rId, String type, int capacity, String availability, double price) {
        this.rId = rId; this.type = type; this.capacity = capacity;
        this.availability = availability; this.pricePerNight = price;
    }
    public int getRId() { return rId; } public void setRId(int v) { this.rId = v; }
    public String getType() { return type; } public void setType(String v) { this.type = v; }
    public int getCapacity() { return capacity; } public void setCapacity(int v) { this.capacity = v; }
    public String getAvailability() { return availability; } public void setAvailability(String v) { this.availability = v; }
    public double getPricePerNight() { return pricePerNight; } public void setPricePerNight(double v) { this.pricePerNight = v; }
}
