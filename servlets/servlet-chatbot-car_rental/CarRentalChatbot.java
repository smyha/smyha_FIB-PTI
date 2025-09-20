package mypackage;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.sql.DataSource;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.HashMap;
import java.util.Map;

@WebServlet("/chat")
public class CarRentalChatbot extends HttpServlet {
    private DataSource dataSource;
    
    @Override
    public void init() throws ServletException {
        try {
            Context initContext = new InitialContext();
            Context envContext = (Context) initContext.lookup("java:/comp/env");
            dataSource = (DataSource) envContext.lookup("jdbc/TestDB");
        } catch (Exception e) {
            throw new ServletException("Failed to initialize database connection", e);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        try {
            // Read the JSON input
            BufferedReader reader = request.getReader();
            JSONParser parser = new JSONParser();
            JSONObject jsonInput = (JSONObject) parser.parse(reader);
            
            String userMessage = (String) jsonInput.get("message");
            String intent = detectIntent(userMessage.toLowerCase());
            
            // Process the message based on intent
            String botResponse = processIntent(intent, userMessage);
            
            // Create JSON response
            JSONObject jsonResponse = new JSONObject();
            jsonResponse.put("response", botResponse);
            
            // Send response
            PrintWriter out = response.getWriter();
            out.print(jsonResponse.toJSONString());
            out.flush();
            
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "An error occurred: " + e.getMessage());
            response.getWriter().write(errorResponse.toJSONString());
        }
    }

    private String detectIntent(String message) {
        if (message.contains("available") || message.contains("rent") || message.contains("car")) {
            return "CHECK_AVAILABILITY";
        } else if (message.contains("price") || message.contains("cost") || message.contains("rate")) {
            return "CHECK_PRICE";
        } else if (message.contains("book") || message.contains("reserve")) {
            return "MAKE_RESERVATION";
        } else {
            return "UNKNOWN";
        }
    }

    private String processIntent(String intent, String message) throws Exception {
        switch (intent) {
            case "CHECK_AVAILABILITY":
                return checkAvailability();
            case "CHECK_PRICE":
                return getPriceInformation();
            case "MAKE_RESERVATION":
                return "To make a reservation, please provide: your name, email, desired car, and rental dates.";
            default:
                return "I'm here to help you rent a car. You can ask about available cars, prices, or make a reservation.";
        }
    }

    private String checkAvailability() throws Exception {
        try (Connection conn = dataSource.getConnection()) {
            String query = "SELECT make, model, year FROM cars WHERE available = true";
            try (PreparedStatement stmt = conn.prepareStatement(query)) {
                ResultSet rs = stmt.executeQuery();
                StringBuilder response = new StringBuilder("Available cars:\n");
                
                while (rs.next()) {
                    response.append(rs.getString("year"))
                           .append(" ")
                           .append(rs.getString("make"))
                           .append(" ")
                           .append(rs.getString("model"))
                           .append("\n");
                }
                
                return response.toString();
            }
        }
    }

    private String getPriceInformation() throws Exception {
        try (Connection conn = dataSource.getConnection()) {
            String query = "SELECT make, model, price_per_day FROM cars WHERE available = true";
            try (PreparedStatement stmt = conn.prepareStatement(query)) {
                ResultSet rs = stmt.executeQuery();
                StringBuilder response = new StringBuilder("Rental rates per day:\n");
                
                while (rs.next()) {
                    response.append(rs.getString("make"))
                           .append(" ")
                           .append(rs.getString("model"))
                           .append(": $")
                           .append(rs.getDouble("price_per_day"))
                           .append("/day\n");
                }
                
                return response.toString();
            }
        }
    }
}