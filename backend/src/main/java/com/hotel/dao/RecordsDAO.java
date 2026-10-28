package com.hotel.dao;

import com.hotel.config.DBConnection;
import com.hotel.model.Records;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class RecordsDAO {
    public List<Records> findAll() throws Exception {
        List<Records> list = new ArrayList<>();
        String sql = "SELECT Record_no, Log_Details, Created_At FROM Records ORDER BY Record_no DESC";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                Records r = new Records();
                r.setRecordNo(rs.getInt("Record_no"));
                r.setLogDetails(rs.getString("Log_Details"));
                Timestamp ts = rs.getTimestamp("Created_At");
                r.setCreatedAt(ts != null ? ts.toString() : null);
                list.add(r);
            }
        }
        return list;
    }

    public int insert(Records r) throws Exception {
        String sql = "INSERT INTO Records (Log_Details) VALUES (?)";
        try (Connection c = DBConnection.getConnection();
             PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, r.getLogDetails());
            ps.executeUpdate();
            try (ResultSet k = ps.getGeneratedKeys()) { if (k.next()) return k.getInt(1); }
        }
        return -1;
    }
}
