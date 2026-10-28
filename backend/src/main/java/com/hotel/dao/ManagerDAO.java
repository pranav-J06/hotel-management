package com.hotel.dao;

import com.hotel.config.DBConnection;
import java.sql.*;
import java.util.*;

public class ManagerDAO {
    public List<Map<String,Object>> findAll() throws Exception {
        List<Map<String,Object>> list = new ArrayList<>();
        String sql = "SELECT m.E_ID, CONCAT(e.First_Name,' ',e.Last_Name) AS Name, m.Department, m.Qualification, e.Salary FROM Manager m JOIN Employee e ON m.E_ID=e.E_ID";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            ResultSetMetaData md = rs.getMetaData();
            while (rs.next()) {
                Map<String,Object> row = new HashMap<>();
                for (int i=1;i<=md.getColumnCount();i++) row.put(md.getColumnLabel(i), rs.getObject(i));
                list.add(row);
            }
        }
        return list;
    }
    public boolean insert(int eId, String dept, String qual) throws Exception {
        String sql = "INSERT INTO Manager (E_ID, Department, Qualification) VALUES (?,?,?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, eId); ps.setString(2, dept); ps.setString(3, qual);
            return ps.executeUpdate() > 0;
        }
    }
}
