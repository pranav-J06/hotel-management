package com.hotel.model;

public class ZipCode {
    private String pinNo;
    private String city;
    private String state;

    public ZipCode() {}
    public ZipCode(String pinNo, String city, String state) { this.pinNo=pinNo; this.city=city; this.state=state; }
    public String getPinNo() { return pinNo; } public void setPinNo(String v) { this.pinNo = v; }
    public String getCity() { return city; } public void setCity(String v) { this.city = v; }
    public String getState() { return state; } public void setState(String v) { this.state = v; }
}
