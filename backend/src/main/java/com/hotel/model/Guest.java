package com.hotel.model;

public class Guest {
    private int gId;
    private String firstName;
    private String lastName;
    private String dob; // YYYY-MM-DD
    private String gender;
    private String mobNo;

    public Guest() {}
    public Guest(int gId, String firstName, String lastName, String dob, String gender, String mobNo) {
        this.gId = gId; this.firstName = firstName; this.lastName = lastName;
        this.dob = dob; this.gender = gender; this.mobNo = mobNo;
    }
    public int getGId() { return gId; } public void setGId(int gId) { this.gId = gId; }
    public String getFirstName() { return firstName; } public void setFirstName(String s) { this.firstName = s; }
    public String getLastName() { return lastName; } public void setLastName(String s) { this.lastName = s; }
    public String getDob() { return dob; } public void setDob(String s) { this.dob = s; }
    public String getGender() { return gender; } public void setGender(String s) { this.gender = s; }
    public String getMobNo() { return mobNo; } public void setMobNo(String s) { this.mobNo = s; }
}
