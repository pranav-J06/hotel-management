package com.hotel.dao;

import com.hotel.config.DBConnection;
import com.hotel.model.ZipCode;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ZipCodeDAO {
    public List<ZipCode> findAll() throws Exception {
        List<ZipCode> list = new ArrayList<>();
        String sql = "SELECT Pin_no, City, State FROM ZipCode";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                ZipCode z = new ZipCode();
                z.setPinNo(rs.getString("Pin_no"));
                z.setCity(rs.getString("City"));
                z.setState(rs.getString("State"));
                list.add(z);
            }
        }
        return list;
    }

    public boolean insert(ZipCode z) throws Exception {
        String sql = "INSERT INTO ZipCode (Pin_no, City, State) VALUES (?,?,?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, z.getPinNo());
            ps.setString(2, z.getCity());
            ps.setString(3, z.getState());
            return ps.executeUpdate() > 0;
        }
    }

    public boolean delete(String pinNo) throws Exception {
        String sql = "DELETE FROM ZipCode WHERE Pin_no=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, pinNo);
            return ps.executeUpdate() > 0;
        }
    }
}
