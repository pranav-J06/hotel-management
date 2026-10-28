package com.hotel.api;

import com.google.gson.Gson;
import com.hotel.dao.BookingDAO;
import com.hotel.model.Booking;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class BookingHandler implements HttpHandler {
    private final BookingDAO dao = new BookingDAO();
    private final Gson gson = new Gson();
    @Override public void handle(HttpExchange ex) throws IOException {
        CorsUtil.addCorsHeaders(ex);
        if (CorsUtil.handleOptions(ex)) return;
        String method = ex.getRequestMethod();
        String query = ex.getRequestURI().getQuery();
        try {
            if ("GET".equals(method)) {
                if (query != null && query.contains("detailed")) {
                    send(ex,200,gson.toJson(dao.findAllDetailed()));
                } else {
                    send(ex,200,gson.toJson(dao.findAll()));
                }
            } else if ("POST".equals(method)) {
                String body = new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
                Booking b = gson.fromJson(body, Booking.class);
                int id = dao.insert(b);
                send(ex,201,"{\"id\":"+id+"}");
            } else if ("DELETE".equals(method)) {
                String path = ex.getRequestURI().getPath();
                int id = Integer.parseInt(path.substring(path.lastIndexOf('/')+1));
                send(ex, dao.delete(id)?200:404, "{\"deleted\":true}");
            } else {
                send(ex,405,"{\"error\":\"Method not allowed\"}");
            }
        } catch (Exception e) {
            e.printStackTrace();
            send(ex,500,"{\"error\":\""+e.getMessage().replace("\"","'")+"\"}");
        }
    }
    private void send(HttpExchange ex,int code,String body) throws IOException {
        byte[] b=body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().add("Content-Type","application/json");
        ex.sendResponseHeaders(code,b.length);
        try(OutputStream os=ex.getResponseBody()){os.write(b);}
    }
}
