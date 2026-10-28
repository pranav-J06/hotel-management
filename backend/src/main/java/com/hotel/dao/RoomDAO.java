package com.hotel.dao;

import com.hotel.config.DBConnection;
import com.hotel.model.Room;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class RoomDAO {

    public List<Room> findAll() throws Exception {
        List<Room> list = new ArrayList<>();
        String sql = "SELECT R_ID, Type, Capacity, Availability, Price_Per_Night FROM Room";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                Room r = new Room();
                r.setRId(rs.getInt("R_ID"));
                r.setType(rs.getString("Type"));
                r.setCapacity(rs.getInt("Capacity"));
                r.setAvailability(rs.getString("Availability"));
                r.setPricePerNight(rs.getDouble("Price_Per_Night"));
                list.add(r);
            }
        }
        return list;
    }

    public List<Room> findAvailable() throws Exception {
        List<Room> list = new ArrayList<>();
        String sql = "SELECT * FROM Room WHERE Availability='Available'";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                Room r = new Room();
                r.setRId(rs.getInt("R_ID"));
                r.setType(rs.getString("Type"));
                r.setCapacity(rs.getInt("Capacity"));
                r.setAvailability(rs.getString("Availability"));
                r.setPricePerNight(rs.getDouble("Price_Per_Night"));
                list.add(r);
            }
        }
        return list;
    }

    public int insert(Room r) throws Exception {
        String sql = "INSERT INTO Room (Type, Capacity, Availability, Price_Per_Night) VALUES (?,?,?,?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, r.getType());
            ps.setInt(2, r.getCapacity());
            ps.setString(3, r.getAvailability());
            ps.setDouble(4, r.getPricePerNight());
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) { if (k.next()) return k.getInt(1); }
        }
        return -1;
    }

    public boolean updateAvailability(int rId, String avail) throws Exception {
        String sql = "UPDATE Room SET Availability=? WHERE R_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, avail);
            ps.setInt(2, rId);
            return ps.executeUpdate() > 0;
        }
    }

    public boolean delete(int id) throws Exception {
        String sql = "DELETE FROM Room WHERE R_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        }
    }
}
