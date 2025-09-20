package mypackage;

import java.io.*;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.sql.*;
import javax.sql.DataSource;
import javax.naming.*;
import java.util.ArrayList;

@WebServlet("/listdb")
public class CarRentalListDB extends HttpServlet {
    
    private void createTableIfNotExists(Connection conn) throws SQLException {
        String createTable = """
            CREATE TABLE IF NOT EXISTS rentals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                engine VARCHAR(50),
                num_vehi INT,
                co2_rating INT,
                descuento DECIMAL(10,2),
                dias_alquiler INT
            )
        """;
        
        try (Statement stmt = conn.createStatement()) {
            stmt.execute(createTable);
        }
    }
    
    private void insertInitialData(Connection conn) throws SQLException {
        // Check if table is empty first
        String countQuery = "SELECT COUNT(*) FROM rentals";
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(countQuery)) {
            rs.next();
            if (rs.getInt(1) > 0) {
                return; // Data already exists
            }
        }
        
        // Insert initial data
        String insertData = """
            INSERT INTO rentals (engine, num_vehi, co2_rating, descuento, dias_alquiler) VALUES
            ('Hybrid', 1, 54, 12.0, 1),
            ('Electric', 2, 71, 23.0, 3),
            ('Hybrid', 1, 54, 0.0, 1),
            ('Hybrid', 1, 71, 0.0, 1),
            ('Electric', 1, 139, 0.0, 1),
            ('Hybrid', 1, 54, 0.0, 1),
            ('Hybrid', 1, 71, 0.0, 1),
            ('Hybrid', 1, 54, 0.0, 1),
            ('Hybrid', 1, 54, 0.0, 1),
            ('Hybrid', 1, 54, 0.0, 1),
            ('Hybrid', 1, 54, 0.0, 1),
            ('Hybrid', 1, 54, 0.0, 1)
        """;
        
        try (Statement stmt = conn.createStatement()) {
            stmt.execute(insertData);
        }
    }
    
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws IOException, ServletException {
        
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        
        try {
            Context initContext = new InitialContext();
            Context envContext = (Context)initContext.lookup("java:/comp/env");
            DataSource ds = (DataSource)envContext.lookup("jdbc/TestDB");
            
            StringBuilder jsonBuilder = new StringBuilder();
            jsonBuilder.append("{\"rentals\":[");
            
            try (Connection conn = ds.getConnection()) {
                // Ensure table exists and has initial data
                createTableIfNotExists(conn);
                insertInitialData(conn);
                
                // Query all rentals
                String query = "SELECT engine, num_vehi, co2_rating, descuento, dias_alquiler FROM rentals";
                try (Statement stmt = conn.createStatement();
                     ResultSet rset = stmt.executeQuery(query)) {
                    
                    boolean first = true;
                    while (rset.next()) {
                        if (!first) {
                            jsonBuilder.append(",");
                        }
                        first = false;
                        
                        jsonBuilder.append("{")
                                 .append("\"engine\":\"").append(rset.getString("engine")).append("\",")
                                 .append("\"num_vehi\":\"").append(rset.getInt("num_vehi")).append("\",")
                                 .append("\"co2_rating\":\"").append(rset.getInt("co2_rating")).append("\",")
                                 .append("\"descuento\":\"").append(rset.getDouble("descuento")).append("\",")
                                 .append("\"dias_alquiler\":\"").append(rset.getInt("dias_alquiler")).append("\"")
                                 .append("}");
                    }
                }
            }
            
            jsonBuilder.append("]}");
            out.println(jsonBuilder.toString());
            
        } catch (Exception ex) {
            response.setStatus(500);
            out.println("{\"error\":\"" + ex.getMessage().replace("\"", "'") + "\"}");
            ex.printStackTrace();
        }
    }
}