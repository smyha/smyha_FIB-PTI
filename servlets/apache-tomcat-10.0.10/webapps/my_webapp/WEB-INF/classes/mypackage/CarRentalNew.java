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
import java.io.IOException;

public class CarRentalNew extends HttpServlet {

  int cont = 0;
 
  // Maneja la creación/actualización del fichero JSON con el nuevo renting (alquiler)
  public void handleCreateRental(String co2Rating, String engine, String dias_alquiler, String num_vehi, Double descuento, PrintWriter out)
   throws ServletException, IOException {
	String relativePath = "/WEB-INF/classes/mypackage/rentals.json";
	File file = new File(getServletContext().getRealPath(relativePath));

	// Asegurar que existe el directorio padre del fichero
	File parentDir = file.getParentFile();
	if (parentDir != null && !parentDir.exists()) {
		parentDir.mkdirs();
	}
	
	JSONObject rentalsObj = null;
	JSONArray rentalsJSON = null;
	
	// Si no existe el fichero, se crea la estructura básica del fichero JSON
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
	
	// Crear el objeto JSON del nuevo renting (alquiler) 
	JSONObject rental = new JSONObject();

	rental.put("co2_rating", co2Rating);
	rental.put("engine", engine);
	rental.put("dias_alquiler", dias_alquiler);
	rental.put("num_vehi", num_vehi);
	rental.put("descuento", String.valueOf(descuento));

	// Añadir a la lista y persistir
	rentalsJSON.add(rental);
			

  		try (FileWriter fileWriter = new FileWriter(file)) {
		
            fileWriter.write(rentalsObj.toJSONString());
			fileWriter.flush();
			out.println("<p>Archivo JSON actualizado exitosamente</p>");
        } catch (IOException e) {
            out.println("<p>Error al escribir JSON: " + e.getMessage() + "</p>");
            e.printStackTrace(new PrintWriter(out));
        }
  }


  public void doGet(HttpServletRequest req, HttpServletResponse res)
                    throws ServletException, IOException {
    res.setContentType("text/html");
    PrintWriter out = res.getWriter();
    
    // Recoger parámetros del formulario
    String co2Rating = req.getParameter("co2_rating");
    String engine = req.getParameter("sub_model_vehicle");
    String dias_alquiler = req.getParameter("dies_lloguer");
    String num_vehi = req.getParameter("num_vehicles");
    String descuento = req.getParameter("descompte");
    										
    // Respuesta HTML con los datos recibidos
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


    handleCreateRental(co2Rating, engine, dias_alquiler, num_vehi, Double.parseDouble(descuento), out);
                     
  }
  

  public void doPost(HttpServletRequest req, HttpServletResponse res)
                    throws ServletException, IOException {
    doGet(req, res);
  }
}


