package com.hotel.model;

public class Records {
    private int recordNo;
    private String logDetails;
    private String createdAt;

    public Records() {}
    public int getRecordNo() { return recordNo; } public void setRecordNo(int v) { this.recordNo = v; }
    public String getLogDetails() { return logDetails; } public void setLogDetails(String v) { this.logDetails = v; }
    public String getCreatedAt() { return createdAt; } public void setCreatedAt(String v) { this.createdAt = v; }
}
