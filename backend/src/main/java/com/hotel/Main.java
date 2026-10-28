package com.hotel;

import com.hotel.api.*;
import com.hotel.config.DBConnection;
import com.hotel.dao.*;
import com.sun.net.httpserver.HttpServer;
import java.io.InputStream;
import java.net.InetSocketAddress;
import java.util.Properties;

public class Main {
    public static void main(String[] args) throws Exception {
        int port = 8080;
        try (InputStream is = DBConnection.class.getClassLoader().getResourceAsStream("db.properties")) {
            if (is != null) {
                Properties p = new Properties(); p.load(is);
                port = Integer.parseInt(p.getProperty("server.port","8080"));
            }
        }
        String envPort = System.getenv("PORT");
        if (envPort != null && !envPort.isBlank()) {
            try {
                port = Integer.parseInt(envPort.trim());
            } catch (NumberFormatException ignored) {}
        }

        // Test DB with retry for containerized / cloud startup
        boolean dbConnected = false;
        for (int attempt = 1; attempt <= 10; attempt++) {
            try {
                DBConnection.getConnection().close();
                System.out.println("✓ DB connection OK");
                dbConnected = true;
                break;
            } catch (Exception e) {
                System.err.println("Waiting for DB connection (attempt " + attempt + "/10): " + e.getMessage());
                if (attempt < 10) {
                    try { Thread.sleep(3000); } catch (InterruptedException ignored) {}
                }
            }
        }
        if (!dbConnected) {
            System.err.println("⚠ Server starting, but DB is not reachable yet.");
        }

        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 0);
        server.createContext("/api/guests", new GuestHandler());
        server.createContext("/api/rooms", new RoomHandler());
        server.createContext("/api/bookings", new BookingHandler());
        server.createContext("/api/employees", new EmployeeHandler());
        server.createContext("/api/bills", new BillHandler());
        server.createContext("/api/zipcodes", new GenericHandler(() -> new ZipCodeDAO().findAll()));
        server.createContext("/api/records", new GenericHandler(() -> new RecordsDAO().findAll()));
        server.createContext("/api/managers", new GenericHandler(() -> new ManagerDAO().findAll()));
        server.createContext("/api/housekeepers", new GenericHandler(() -> new HousekeeperDAO().findAll()));
        server.createContext("/api/receptionists", new GenericHandler(() -> new ReceptionistDAO().findAll()));
        server.createContext("/api/housekeeper-rooms", new GenericHandler(() -> new HousekeeperDAO().findAssignments()));
        // Health check
        server.createContext("/api/health", ex -> {
            ex.getResponseHeaders().add("Access-Control-Allow-Origin","*");
            String res = "{\"status\":\"UP\",\"db\":\"hotel_management\"}";
            ex.getResponseHeaders().add("Content-Type","application/json");
            ex.sendResponseHeaders(200,res.length());
            ex.getResponseBody().write(res.getBytes());
            ex.getResponseBody().close();
        });

        server.setExecutor(null);
        server.start();
        System.out.println("Hotel Management API running at http://localhost:"+port);
        System.out.println("Endpoints: /api/guests /api/rooms /api/bookings /api/employees /api/bills /api/zipcodes /api/records /api/managers /api/housekeepers /api/receptionists /api/housekeeper-rooms /api/health");
    }
}
