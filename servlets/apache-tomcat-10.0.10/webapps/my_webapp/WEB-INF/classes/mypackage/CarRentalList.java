package mypackage;

import java.io.*;
import jakarta.servlet.*;
import jakarta.servlet.http.*;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Iterator;

import java.io.FileWriter;
import jakarta.servlet.http.HttpSession;

public class CarRentalList extends HttpServlet {

  int cont = 0;

  public void doGet(HttpServletRequest req, HttpServletResponse res)
                    throws ServletException, IOException {
    
    res.setContentType("text/html");
    PrintWriter out = res.getWriter();
    
    String username = req.getParameter("userid");
    String passw = req.getParameter("password");

    if (username != null) username = username.trim();
    if (passw != null) passw = passw.trim();

    String user= "admin";
    String pass= "1234";
    
    if(username != null && passw != null && username.equalsIgnoreCase(user) && pass.equals(passw)){
  		handleReadRental(res);
    }else{
		out.println("<html><body><big>User = admin</big><br><br> <big>pass = 1234</big>"+
                  "<br><br><small>Received userid=\"" + (username==null?"null":username) + "\" password=\"" 
                  + (passw==null?"null":passw) + "\"</small></body></html>");
  	}

    
  }

  public void handleReadRental(HttpServletResponse res) {
    JSONParser parser = new JSONParser();
    
    try {    
        res.setContentType("text/html");
        PrintWriter out = res.getWriter();
        
        out.println("<html>");
        out.println("<head>");
        out.println("<title>Rental List</title>");
        out.println("<style>");
        out.println(".rental-item { margin-bottom: 20px; padding: 10px; border: 1px solid #ccc; }");
        out.println(".rental-item label { font-weight: bold; width: 150px; display: inline-block; }");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");
        
        out.println("<h1>Rental List:</h1>");
        
        String relativePath = "/WEB-INF/classes/mypackage/rentals.json";
        File file = new File(getServletContext().getRealPath(relativePath));
        
        Object obj = parser.parse(new FileReader(file));
        JSONObject jsonObject = (JSONObject) obj;
        JSONArray rentals = (JSONArray) jsonObject.get("rentals");
        
        // Iterate through the rentals array
        for (Object rentalObj : rentals) {
            JSONObject rental = (JSONObject) rentalObj;
            out.println("<div class='rental-item'>");
            String co2 = String.valueOf(rental.get("co2_rating"));
            String engine = String.valueOf(rental.get("engine"));
            String days = rental.get("dias_alquiler") != null ? String.valueOf(rental.get("dias_alquiler")) : String.valueOf(rental.get("days"));
            String units = rental.get("num_vehi") != null ? String.valueOf(rental.get("num_vehi")) : String.valueOf(rental.get("units"));
            String discount = rental.get("descuento") != null ? String.valueOf(rental.get("descuento")) : String.valueOf(rental.get("discount"));

            out.println("<p><label>CO2 Rating:</label> " + co2 + "</p>");
            out.println("<p><label>Engine:</label> " + engine + "</p>");
            out.println("<p><label>Number of days:</label> " + days + "</p>");
            out.println("<p><label>Number of units:</label> " + units + "</p>");
            out.println("<p><label>Discount:</label> " + discount + "</p>");
            out.println("<hr>");
            out.println("</div>");
        }
        
        // Add back to home link
        out.println("<br><a href='carrental_home.html'>Back to Home</a>");
        out.println("</body></html>");

    } catch (Exception e) {
        try {
            PrintWriter out = res.getWriter();
            out.println("<html><body>");
            out.println("<h1>Error</h1>");
            out.println("<p>Error reading JSON file: " + e.getMessage() + "</p>");
            out.println("<a href='carrental_home.html'>Back to Home</a>");
            out.println("</body></html>");
            e.printStackTrace(new PrintWriter(out));
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }
  }

  public void doPost(HttpServletRequest req, HttpServletResponse res)
        throws ServletException, IOException {
    doGet(req, res);
  }
}


