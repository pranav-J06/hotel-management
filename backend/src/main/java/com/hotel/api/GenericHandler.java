package com.hotel.api;

import com.google.gson.Gson;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Callable;

public class GenericHandler implements HttpHandler {
    private final Callable<Object> getFn;
    private final Gson gson = new Gson();

    public GenericHandler(Callable<Object> getFn) { this.getFn = getFn; }

    @Override public void handle(HttpExchange ex) throws IOException {
        CorsUtil.addCorsHeaders(ex);
        if (CorsUtil.handleOptions(ex)) return;
        try {
            if ("GET".equals(ex.getRequestMethod())) {
                send(ex,200,gson.toJson(getFn.call()));
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
