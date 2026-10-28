package com.hotel.dao;

import com.hotel.config.DBConnection;
import com.hotel.model.Bill;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class BillDAO {
    public List<Bill> findAll() throws Exception {
        List<Bill> list = new ArrayList<>();
        String sql = "SELECT B_ID, G_ID, Amount, Billing_Date, Payment_Status, Booking_ID FROM Bill ORDER BY B_ID DESC";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                Bill b = new Bill();
                b.setBId(rs.getInt("B_ID"));
                b.setGId(rs.getInt("G_ID"));
                b.setAmount(rs.getDouble("Amount"));
                Date d = rs.getDate("Billing_Date");
                b.setBillingDate(d != null ? d.toString() : null);
                b.setPaymentStatus(rs.getString("Payment_Status"));
                int bk = rs.getInt("Booking_ID");
                b.setBookingId(rs.wasNull() ? null : bk);
                list.add(b);
            }
        }
        return list;
    }

    public int insert(Bill b) throws Exception {
        String sql = "INSERT INTO Bill (G_ID, Amount, Billing_Date, Payment_Status, Booking_ID) VALUES (?,?,?,?,?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, b.getGId());
            ps.setDouble(2, b.getAmount());
            ps.setDate(3, b.getBillingDate() != null ? Date.valueOf(b.getBillingDate()) : Date.valueOf(java.time.LocalDate.now().toString()));
            ps.setString(4, b.getPaymentStatus() != null ? b.getPaymentStatus() : "Unpaid");
            if (b.getBookingId() != null) ps.setInt(5, b.getBookingId()); else ps.setNull(5, Types.INTEGER);
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) { if (k.next()) return k.getInt(1); }
        }
        return -1;
    }

    public boolean updateStatus(int bId, String status) throws Exception {
        String sql = "UPDATE Bill SET Payment_Status=? WHERE B_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, status);
            ps.setInt(2, bId);
            return ps.executeUpdate() > 0;
        }
    }

    public boolean delete(int id) throws Exception {
        String sql = "DELETE FROM Bill WHERE B_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        }
    }
}
