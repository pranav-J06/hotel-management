package com.hotel.api;

import com.sun.net.httpserver.HttpExchange;

public class CorsUtil {
    public static void addCorsHeaders(HttpExchange ex) {
        ex.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
        ex.getResponseHeaders().add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        ex.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }
    public static boolean handleOptions(HttpExchange ex) throws java.io.IOException {
        if ("OPTIONS".equalsIgnoreCase(ex.getRequestMethod())) {
            addCorsHeaders(ex);
            ex.sendResponseHeaders(204, -1);
            return true;
        }
        return false;
    }
}
