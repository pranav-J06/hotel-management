package com.hotel.model;

public class Employee {
    private int eId;
    private String firstName;
    private String lastName;
    private double salary;
    private String sex;
    private String mobNo;
    private String pinNo;
    // extra for join view
    private String city;
    private String state;
    private String role;

    public Employee() {}
    public int getEId() { return eId; } public void setEId(int v) { this.eId = v; }
    public String getFirstName() { return firstName; } public void setFirstName(String v) { this.firstName = v; }
    public String getLastName() { return lastName; } public void setLastName(String v) { this.lastName = v; }
    public double getSalary() { return salary; } public void setSalary(double v) { this.salary = v; }
    public String getSex() { return sex; } public void setSex(String v) { this.sex = v; }
    public String getMobNo() { return mobNo; } public void setMobNo(String v) { this.mobNo = v; }
    public String getPinNo() { return pinNo; } public void setPinNo(String v) { this.pinNo = v; }
    public String getCity() { return city; } public void setCity(String v) { this.city = v; }
    public String getState() { return state; } public void setState(String v) { this.state = v; }
    public String getRole() { return role; } public void setRole(String v) { this.role = v; }
}
