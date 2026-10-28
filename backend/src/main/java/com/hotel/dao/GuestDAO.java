package com.hotel.dao;

import com.hotel.config.DBConnection;
import com.hotel.model.Guest;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class GuestDAO {

    public List<Guest> findAll() throws Exception {
        List<Guest> list = new ArrayList<>();
        String sql = "SELECT G_ID, First_Name, Last_Name, DOB, Gender, Mob_No FROM Guest";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                Guest g = new Guest();
                g.setGId(rs.getInt("G_ID"));
                g.setFirstName(rs.getString("First_Name"));
                g.setLastName(rs.getString("Last_Name"));
                Date dob = rs.getDate("DOB");
                g.setDob(dob != null ? dob.toString() : null);
                g.setGender(rs.getString("Gender"));
                g.setMobNo(rs.getString("Mob_No"));
                list.add(g);
            }
        }
        return list;
    }

    public Guest findById(int id) throws Exception {
        String sql = "SELECT * FROM Guest WHERE G_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    Guest g = new Guest();
                    g.setGId(rs.getInt("G_ID"));
                    g.setFirstName(rs.getString("First_Name"));
                    g.setLastName(rs.getString("Last_Name"));
                    Date dob = rs.getDate("DOB");
                    g.setDob(dob != null ? dob.toString() : null);
                    g.setGender(rs.getString("Gender"));
                    g.setMobNo(rs.getString("Mob_No"));
                    return g;
                }
            }
        }
        return null;
    }

    public int insert(Guest g) throws Exception {
        String sql = "INSERT INTO Guest (First_Name, Last_Name, DOB, Gender, Mob_No) VALUES (?,?,?,?,?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, g.getFirstName());
            ps.setString(2, g.getLastName());
            ps.setDate(3, (g.getDob() != null && !g.getDob().isEmpty()) ? Date.valueOf(g.getDob()) : null);
            ps.setString(4, g.getGender());
            ps.setString(5, g.getMobNo());
            ps.executeUpdate();
            try (ResultSet keys = ps.getGeneratedKeys()) {
                if (keys.next()) return keys.getInt(1);
            }
        }
        return -1;
    }

    public boolean update(Guest g) throws Exception {
        String sql = "UPDATE Guest SET First_Name=?, Last_Name=?, DOB=?, Gender=?, Mob_No=? WHERE G_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, g.getFirstName());
            ps.setString(2, g.getLastName());
            ps.setDate(3, (g.getDob() != null && !g.getDob().isEmpty()) ? Date.valueOf(g.getDob()) : null);
            ps.setString(4, g.getGender());
            ps.setString(5, g.getMobNo());
            ps.setInt(6, g.getGId());
            return ps.executeUpdate() > 0;
        }
    }

    public boolean delete(int id) throws Exception {
        String sql = "DELETE FROM Guest WHERE G_ID=?";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        }
    }
}
