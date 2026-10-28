package com.hotel.api;

import com.google.gson.Gson;
import com.hotel.dao.BillDAO;
import com.hotel.model.Bill;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class BillHandler implements HttpHandler {
    private final BillDAO dao = new BillDAO();
    private final Gson gson = new Gson();
    @Override public void handle(HttpExchange ex) throws IOException {
        CorsUtil.addCorsHeaders(ex);
        if (CorsUtil.handleOptions(ex)) return;
        try {
            String method = ex.getRequestMethod();
            if ("GET".equals(method)) send(ex,200,gson.toJson(dao.findAll()));
            else if ("POST".equals(method)) {
                String body=new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
                Bill b=gson.fromJson(body, Bill.class);
                int id=dao.insert(b);
                send(ex,201,"{\"id\":"+id+"}");
            } else if ("DELETE".equals(method)) {
                int id=Integer.parseInt(ex.getRequestURI().getPath().substring(ex.getRequestURI().getPath().lastIndexOf('/')+1));
                send(ex,dao.delete(id)?200:404,"{\"deleted\":true}");
            } else send(ex,405,"{\"error\":\"Method not allowed\"}");
        } catch(Exception e){ e.printStackTrace(); send(ex,500,"{\"error\":\""+e.getMessage().replace("\"","'")+"\"}"); }
    }
    private void send(HttpExchange ex,int code,String body) throws IOException {
        byte[] b=body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().add("Content-Type","application/json");
        ex.sendResponseHeaders(code,b.length);
        try(OutputStream os=ex.getResponseBody()){os.write(b);}
    }
}
