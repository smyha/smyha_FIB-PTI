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

// Servlet to list car rentals from a JSON file
public class CarRentalList extends HttpServlet {


  // Handles GET requests to display the rental list (with simple authentication)
  public void doGet(HttpServletRequest req, HttpServletResponse res)
                    throws ServletException, IOException {
    
    res.setContentType("text/html");
    PrintWriter out = res.getWriter();
    
    // Retrieve username and password from request parameters
    String username = req.getParameter("userid");
    String passw = req.getParameter("password");

    // Trim whitespace from username and password if not null
    if (username != null) username = username.trim();
    if (passw != null) passw = passw.trim();

    // Hardcoded credentials for authentication
    String user= "admin";
    String pass= "1234";
    
    // Check if credentials are correct
    if(username != null && passw != null && username.equalsIgnoreCase(user) && pass.equals(passw)){
  		handleReadRental(res); // If correct, show rental list
    }else{
    // If incorrect, show info and what was received
    out.println("<html><body><big>User = admin</big><br><br> <big>pass = 1234</big>"+
                "<br><br><small>Received userid=\"" + (username==null?"null":username) + "\" password=\"" 
                + (passw==null?"null":passw) + "\"</small></body></html>");
  	}

    
  }

  // Reads the rentals.json file and displays the list of rentals in HTML
  public void handleReadRental(HttpServletResponse res) {
    JSONParser parser = new JSONParser();
    
    try {    
        res.setContentType("text/html");
        PrintWriter out = res.getWriter();
        
        // Start HTML output
        out.println("<html>");
        out.println("<head>");
        out.println("<title>Rental List</title>");
        // Add some CSS for styling the rental items
        out.println("<style>");
        out.println(".rental-item { margin-bottom: 20px; padding: 10px; border: 1px solid #ccc; }");
        out.println(".rental-item label { font-weight: bold; width: 150px; display: inline-block; }");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");
        
        out.println("<h1>Rental List:</h1>");
        
        // Path to the JSON file containing rentals
        String relativePath = "/WEB-INF/classes/mypackage/rentals.json";
        File file = new File(getServletContext().getRealPath(relativePath));
        
        // Parse the JSON file
        Object obj = parser.parse(new FileReader(file));
        JSONObject jsonObject = (JSONObject) obj;
        JSONArray rentals = (JSONArray) jsonObject.get("rentals");
        
        // Iterate through the rentals array and print each rental's details
        for (Object rentalObj : rentals) {
            JSONObject rental = (JSONObject) rentalObj;
            out.println("<div class='rental-item'>");
            // Obtain the fileds of the renting 
            String co2 = String.valueOf(rental.get("co2_rating"));
            String engine = String.valueOf(rental.get("engine"));
            String days = String.valueOf(rental.get("dias_alquiler"));
            String units = String.valueOf(rental.get("num_vehi"));
            String discount = String.valueOf(rental.get("descuento"));

            // Output rental details
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
        // Handle errors reading or parsing the JSON file
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

  // Handles POST requests by delegating to doGet (same behavior)
  public void doPost(HttpServletRequest req, HttpServletResponse res)
        throws ServletException, IOException {
    doGet(req, res);
  }
}
