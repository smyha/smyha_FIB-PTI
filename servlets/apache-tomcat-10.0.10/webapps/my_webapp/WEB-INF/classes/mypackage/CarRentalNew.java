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

public class CarRentalNew extends HttpServlet {

  // Counter for the number of accesses to the servlet
  int cont = 0;	
 
  // Handles the creation/update of the JSON file with the new rental
  public void handleCreateRental(String co2Rating, String engine, String dias_alquiler, String num_vehi, Double descuento, PrintWriter out)
   throws ServletException, IOException {
	String relativePath = "/WEB-INF/classes/mypackage/rentals.json";
	File file = new File(getServletContext().getRealPath(relativePath));

	// Ensure the parent directory of the file exists
	File parentDir = file.getParentFile();
	if (parentDir != null && !parentDir.exists()) {
		parentDir.mkdirs();
	}
	
	JSONObject rentalsObj = null;
	JSONArray rentalsJSON = null;
	
	// If the file does not exist, create the basic structure of the JSON file
	if(!file.exists() || file.isDirectory()) { 
		out.println("<p>Creando nuevo archivo JSON</p>");
		rentalsObj = new JSONObject();
		rentalsJSON = new JSONArray();
		rentalsObj.put("rentals", rentalsJSON);
	} else {
		out.println("<p>Actualizando archivo JSON existente</p>");
		JSONParser parser = new JSONParser();
		try {
			rentalsObj = (JSONObject) parser.parse(new FileReader(file));
			rentalsJSON = (JSONArray) rentalsObj.get("rentals");
		} catch (Exception e) {
			out.println("<p>Error al leer JSON: " + e.getMessage() + "</p>");
			e.printStackTrace(new PrintWriter(out));
			return;
		}
	}
	
	// Create the JSON object for the new rental
	JSONObject rental = new JSONObject();

	rental.put("co2_rating", co2Rating);
	rental.put("engine", engine);
	rental.put("dias_alquiler", dias_alquiler);
	rental.put("num_vehi", num_vehi);
	rental.put("descuento", String.valueOf(descuento));

	// Add to the list and persist
	rentalsJSON.add(rental);
			
	// Write the updated JSON object to the file
	try (FileWriter fileWriter = new FileWriter(file)) {
	
		fileWriter.write(rentalsObj.toJSONString());
		fileWriter.flush();
		out.println("<p>Archivo JSON actualizado exitosamente</p>");
	} catch (IOException e) {
		out.println("<p>Error al escribir JSON: " + e.getMessage() + "</p>");
		e.printStackTrace(new PrintWriter(out));
	}
  }

  // Handles GET requests to create a new rental (with HTML response and form data)
  public void doGet(HttpServletRequest req, HttpServletResponse res)
                    throws ServletException, IOException {
    res.setContentType("text/html");
    PrintWriter out = res.getWriter();
    
    // Collect parameters from the form
    String co2Rating = req.getParameter("co2_rating");
    String engine = req.getParameter("sub_model_vehicle");
    String dias_alquiler = req.getParameter("dies_lloguer");
    String num_vehi = req.getParameter("num_vehicles");
    String descuento = req.getParameter("descompte");
    										
    // HTML response with the received data
    out.println("<html>" +
    "<head><title>Detalles de Alquiler</title></head>" +
    "<body>" +
    	"<h1>Detalles del Alquiler del Vehículo</h1>" +
    	"<p>CO2 Rating: " + co2Rating + "</p>" +
    	"<p>Engine: " + engine + "</p>" +
    	"<p>Días de Alquiler: " + dias_alquiler + "</p>" +
    	"<p>Número de Vehículos: " + num_vehi + "</p>" +
    	"<p>Descuento: " + descuento + "</p>" +
    	"<hr/>" +
    	"<br><br><a href='carrental_home.html'>Home</a>" +
    "</body>" +
    "</html>");

	// Create the rental
    handleCreateRental(co2Rating, engine, dias_alquiler, num_vehi, Double.parseDouble(descuento), out);
                     
  }
  
  public void doPost(HttpServletRequest req, HttpServletResponse res)
                    throws ServletException, IOException {
    doGet(req, res);
  }
}
