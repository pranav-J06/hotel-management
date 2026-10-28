package com.hotel.dao;

import com.hotel.config.DBConnection;
import com.hotel.model.Employee;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class EmployeeDAO {

    public List<Employee> findAll() throws Exception {
        List<Employee> list = new ArrayList<>();
        String sql = "SELECT * FROM vw_employee_details";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                Employee e = new Employee();
                e.setEId(rs.getInt("E_ID"));
                String full = rs.getString("Full_Name");
                if (full != null) {
                    String[] parts = full.split(" ", 2);
                    e.setFirstName(parts[0]);
                    e.setLastName(parts.length > 1 ? parts[1] : "");
                }
                e.setSalary(rs.getDouble("Salary"));
                e.setSex(rs.getString("Sex"));
                e.setMobNo(rs.getString("Mob_No"));
                e.setPinNo(rs.getString("Pin_no"));
                e.setCity(rs.getString("City"));
                e.setState(rs.getString("State"));
                e.setRole(rs.getString("Role"));
                list.add(e);
            }
        }
        return list;
    }

    public Employee findById(int id) throws Exception {
        String sql = "SELECT E_ID, First_Name, Last_Name, Salary, Sex, Mob_No, Pin_no FROM Employee WHERE E_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    Employee e = new Employee();
                    e.setEId(rs.getInt("E_ID"));
                    e.setFirstName(rs.getString("First_Name"));
                    e.setLastName(rs.getString("Last_Name"));
                    e.setSalary(rs.getDouble("Salary"));
                    e.setSex(rs.getString("Sex"));
                    e.setMobNo(rs.getString("Mob_No"));
                    e.setPinNo(rs.getString("Pin_no"));
                    return e;
                }
            }
        }
        return null;
    }

    public int insert(Employee e) throws Exception {
        String sql = "INSERT INTO Employee (First_Name, Last_Name, Salary, Sex, Mob_No, Pin_no) VALUES (?,?,?,?,?,?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, e.getFirstName());
            ps.setString(2, e.getLastName());
            ps.setDouble(3, e.getSalary());
            ps.setString(4, e.getSex());
            ps.setString(5, e.getMobNo());
            ps.setString(6, e.getPinNo());
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) { if (k.next()) return k.getInt(1); }
        }
        return -1;
    }

    public boolean delete(int id) throws Exception {
        String sql = "DELETE FROM Employee WHERE E_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        }
    }
}
