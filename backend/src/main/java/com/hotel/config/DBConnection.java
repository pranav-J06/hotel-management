package com.hotel.config;

import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Properties;

public class DBConnection {
    private static String URL;
    private static String USER;
    private static String PASSWORD;
    private static String DRIVER;

    static {
        try (InputStream is = DBConnection.class.getClassLoader().getResourceAsStream("db.properties")) {
            Properties props = new Properties();
            if (is != null) {
                props.load(is);
            }

            // Environment variables override properties file (essential for Cloud/Docker)
            String envUrl = System.getenv("DB_URL");
            String envHost = System.getenv("DB_HOST");
            String envPort = System.getenv("DB_PORT");
            String envName = System.getenv("DB_NAME");

            if (envUrl != null && !envUrl.isBlank()) {
                URL = envUrl;
            } else if (envHost != null && !envHost.isBlank()) {
                String port = (envPort != null && !envPort.isBlank()) ? envPort : "3306";
                String db = (envName != null && !envName.isBlank()) ? envName : "hotel_management";
                URL = "jdbc:mysql://" + envHost + ":" + port + "/" + db + "?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";
            } else {
                URL = props.getProperty("db.url", "jdbc:mysql://localhost:3306/hotel_management?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC");
            }

            String envUser = System.getenv("DB_USER");
            USER = (envUser != null && !envUser.isBlank()) ? envUser : props.getProperty("db.user", "root");

            String envPass = System.getenv("DB_PASSWORD");
            PASSWORD = (envPass != null) ? envPass : props.getProperty("db.password", "root");

            DRIVER = props.getProperty("db.driver", "com.mysql.cj.jdbc.Driver");
            Class.forName(DRIVER);
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to load DB config", e);
        }
    }

    public static Connection getConnection() throws Exception {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }

    // Test connection
    public static void main(String[] args) throws Exception {
        try (Connection c = getConnection()) {
            System.out.println("DB Connected: " + c.getMetaData().getURL());
        }
    }
}
