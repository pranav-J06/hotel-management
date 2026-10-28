package com.hotel.api;

import com.google.gson.Gson;
import com.hotel.dao.GuestDAO;
import com.hotel.model.Guest;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class GuestHandler implements HttpHandler {
    private final GuestDAO dao = new GuestDAO();
    private final Gson gson = new Gson();

    @Override public void handle(HttpExchange ex) throws IOException {
        CorsUtil.addCorsHeaders(ex);
        if (CorsUtil.handleOptions(ex)) return;
        String method = ex.getRequestMethod();
        String path = ex.getRequestURI().getPath(); // /api/guests or /api/guests/1
        try {
            if ("GET".equals(method)) {
                if (path.matches(".*/\\d+$")) {
                    int id = Integer.parseInt(path.substring(path.lastIndexOf('/')+1));
                    Guest g = dao.findById(id);
                    send(ex, 200, gson.toJson(g));
                } else {
                    send(ex, 200, gson.toJson(dao.findAll()));
                }
            } else if ("POST".equals(method)) {
                String body = new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
                Guest g = gson.fromJson(body, Guest.class);
                int id = dao.insert(g);
                send(ex, 201, "{\"id\":"+id+"}");
            } else if ("PUT".equals(method)) {
                String body = new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
                Guest g = gson.fromJson(body, Guest.class);
                boolean ok = dao.update(g);
                send(ex, ok?200:404, "{\"updated\":"+ok+"}");
            } else if ("DELETE".equals(method)) {
                int id = Integer.parseInt(path.substring(path.lastIndexOf('/')+1));
                boolean ok = dao.delete(id);
                send(ex, ok?200:404, "{\"deleted\":"+ok+"}");
            } else {
                send(ex, 405, "{\"error\":\"Method not allowed\"}");
            }
        } catch (Exception e) {
            e.printStackTrace();
            send(ex, 500, "{\"error\":\""+e.getMessage().replace("\"","'")+"\"}");
        }
    }
    private void send(HttpExchange ex, int code, String body) throws IOException {
        byte[] b = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().add("Content-Type","application/json");
        ex.sendResponseHeaders(code, b.length);
        try (OutputStream os = ex.getResponseBody()) { os.write(b); }
    }
}
