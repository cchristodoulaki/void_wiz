package controlLayer;

/**
 * @author Giorgos Anestis, TUC/MUSIC
 *  
 * This package contains basic logging implementation 
 * 
 * It is currently a wrapper of the default java logging classes
 *  
 * @version 1.0
 * 
 * Copyright 2008 Giorgos Anestis. All Rights Reserved.
 * 
 * All of the documentation and software, both binary and source is copyrighted 
 * by the author. Redistribution and use in source or binary forms, with or 
 * without modification, are NOT permitted. Any user wishing to make use of the 
 * Software must contact the author to arrange an appropriate license.
 */



import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;

/**
 * Interface for Action objects 
 * 
 * <p>This interface is used to provide a generic interface to Action objects, 
 * which are used to implement a request action. Action object are actually 
 * commnad objects</p> 
 *
 * <p> The Action interface defines three core methods: execute, getView and
 * getModel</p>
 *
 * <p>The execute method, when implemented, will perform any necessary business
 * logic needed to carry out the request</p>
 *
 * <p>The getView and getModel methods are used to return the page and data
 * necessary to present the results of the action</p>
 */

public interface Action {
   
  
   /** Execute business logic */
   public boolean execute(HttpServletRequest req, HttpServletResponse res)
     throws ServletException, IOException;
   
   /** Return the page name (and path) to display the view */
   public String getView();
   
   /** Return a JavaBean containing the model (data) */
   public Object getModel();   
}
