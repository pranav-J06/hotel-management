package com.hotel.dao;

import com.hotel.config.DBConnection;
import com.hotel.model.Booking;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class BookingDAO {

    public List<Booking> findAll() throws Exception {
        List<Booking> list = new ArrayList<>();
        String sql = "SELECT * FROM Booking_Record ORDER BY Booking_ID DESC";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                Booking b = map(rs);
                list.add(b);
            }
        }
        return list;
    }

    // Join view for frontend
    public List<java.util.Map<String,Object>> findAllDetailed() throws Exception {
        List<java.util.Map<String,Object>> list = new ArrayList<>();
        String sql = "SELECT * FROM vw_booking_details";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            ResultSetMetaData md = rs.getMetaData();
            while (rs.next()) {
                java.util.Map<String,Object> row = new java.util.HashMap<>();
                for (int i=1; i<=md.getColumnCount(); i++) row.put(md.getColumnLabel(i), rs.getObject(i));
                list.add(row);
            }
        }
        return list;
    }

    public int insert(Booking b) throws Exception {
        String sql = "INSERT INTO Booking_Record (G_ID, R_ID, Booking_Type, Status, Check_In, Check_Out) VALUES (?,?,?,?,?,?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, b.getGId());
            ps.setInt(2, b.getRId());
            ps.setString(3, b.getBookingType());
            ps.setString(4, b.getStatus());
            ps.setDate(5, Date.valueOf(b.getCheckIn()));
            ps.setDate(6, Date.valueOf(b.getCheckOut()));
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) { if (k.next()) return k.getInt(1); }
        }
        return -1;
    }

    public boolean updateStatus(int bookingId, String status) throws Exception {
        String sql = "UPDATE Booking_Record SET Status=? WHERE Booking_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, status);
            ps.setInt(2, bookingId);
            return ps.executeUpdate() > 0;
        }
    }

    public boolean delete(int id) throws Exception {
        String sql = "DELETE FROM Booking_Record WHERE Booking_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        }
    }

    private Booking map(ResultSet rs) throws SQLException {
        Booking b = new Booking();
        b.setBookingId(rs.getInt("Booking_ID"));
        b.setGId(rs.getInt("G_ID"));
        b.setRId(rs.getInt("R_ID"));
        b.setBookingType(rs.getString("Booking_Type"));
        b.setStatus(rs.getString("Status"));
        Date ci = rs.getDate("Check_In");
        Date co = rs.getDate("Check_Out");
        b.setCheckIn(ci != null ? ci.toString() : null);
        b.setCheckOut(co != null ? co.toString() : null);
        return b;
    }
}
