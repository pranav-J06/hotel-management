package com.hotel.dao;

import com.hotel.config.DBConnection;
import java.sql.*;
import java.util.*;

public class ReceptionistDAO {
    public List<Map<String,Object>> findAll() throws Exception {
        String sql="SELECT r.E_ID, CONCAT(e.First_Name,' ',e.Last_Name) AS Name FROM Receptionist r JOIN Employee e ON r.E_ID=e.E_ID";
        return queryList(sql);
    }
    public boolean insert(int eId) throws Exception {
        String sql="INSERT INTO Receptionist (E_ID) VALUES (?)";
        try(Connection c=DBConnection.getConnection(); PreparedStatement ps=c.prepareStatement(sql)){ ps.setInt(1,eId); return ps.executeUpdate()>0; }
    }
    public List<Map<String,Object>> findRecords() throws Exception {
        String sql="SELECT rr.E_ID, CONCAT(e.First_Name,' ',e.Last_Name) AS Receptionist, rr.Record_no, rec.Log_Details FROM Receptionist_Records rr JOIN Employee e ON rr.E_ID=e.E_ID JOIN Records rec ON rr.Record_no=rec.Record_no";
        return queryList(sql);
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
