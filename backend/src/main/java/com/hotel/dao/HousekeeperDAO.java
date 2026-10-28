package com.hotel.dao;

import com.hotel.config.DBConnection;
import java.sql.*;
import java.util.*;

public class HousekeeperDAO {
    public List<Map<String,Object>> findAll() throws Exception {
        List<Map<String,Object>> list = new ArrayList<>();
        String sql = "SELECT h.E_ID, CONCAT(e.First_Name,' ',e.Last_Name) AS Name, e.Mob_No FROM Housekeeper h JOIN Employee e ON h.E_ID=e.E_ID";
        try (Connection c = DBConnection.getConnection();
             Statement st = c.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            ResultSetMetaData md = rs.getMetaData();
            while (rs.next()) { Map<String,Object> row=new HashMap<>(); for(int i=1;i<=md.getColumnCount();i++) row.put(md.getColumnLabel(i), rs.getObject(i)); list.add(row); }
        }
        return list;
    }
    public boolean insert(int eId) throws Exception {
        String sql="INSERT INTO Housekeeper (E_ID) VALUES (?)";
        try(Connection c=DBConnection.getConnection(); PreparedStatement ps=c.prepareStatement(sql)){ ps.setInt(1,eId); return ps.executeUpdate()>0; }
    }
    // Junction: Housekeeper_Room
    public List<Map<String,Object>> findAssignments() throws Exception {
        String sql="SELECT hr.E_ID, CONCAT(e.First_Name,' ',e.Last_Name) AS Housekeeper, hr.R_ID, r.Type FROM Housekeeper_Room hr JOIN Employee e ON hr.E_ID=e.E_ID JOIN Room r ON hr.R_ID=r.R_ID";
        return queryList(sql);
    }
    public boolean assignRoom(int eId, int rId) throws Exception {
        String sql="INSERT INTO Housekeeper_Room (E_ID, R_ID) VALUES (?,?)";
        try(Connection c=DBConnection.getConnection(); PreparedStatement ps=c.prepareStatement(sql)){ ps.setInt(1,eId); ps.setInt(2,rId); return ps.executeUpdate()>0; }
    }
    private List<Map<String,Object>> queryList(String sql) throws Exception{
        List<Map<String,Object>> list=new ArrayList<>();
        try(Connection c=DBConnection.getConnection(); Statement st=c.createStatement(); ResultSet rs=st.executeQuery(sql)){
            ResultSetMetaData md=rs.getMetaData();
            while(rs.next()){ Map<String,Object> row=new HashMap<>(); for(int i=1;i<=md.getColumnCount();i++) row.put(md.getColumnLabel(i), rs.getObject(i)); list.add(row); }
        }
        return list;
    }
}
