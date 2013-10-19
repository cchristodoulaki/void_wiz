package controlLayer;

/**
 * @author Giorgos Anestis, TUC/MUSIC
 *  
 * This package contains basic and well known design patterns implementation 
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



import controlLayer.Action;
import controlLayer.ActionFactory;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;
import java.util.HashMap;

/**
 * Request helper utility
 *
 * <p>Used simply to extract the 'Action' parameter and then return the 
 * appropriate Action class using the ActionFactory. This class could be used 
 * to assist with any request handling activity that can be offloaded from the 
 * servlet.</p>
 *
 * <p>It accepts a request object in its constructor and wraps the request with
 * additional functionality that may be needed to process the request such as
 * parsing the request parameters or determining the action the servlet should
 * take </p>
 */

public class RequestUtility {
   
   /** Local copy of request object. */
   HttpServletRequest request;
   HashMap actions;
   /**
    * Constructor. Used to set local request object.
    */
   public RequestUtility(HttpServletRequest req, HashMap actions) 
                      throws ServletException, IOException {
      this.request = req;
      this.actions = actions;
   }

   /**
    * Use factory to create action based on request parms
    */
   public Action getAction() {
           
      String action = (String)request.getParameter("action"); 
      
      if (action != null) {
        String actionClass = (String)actions.get(action);
      
        if ( actionClass != null)
          return ActionFactory.createAction(actionClass);
      }
      else {
        String actionClass = (String)actions.get("loadFirstPage");
      
        if ( actionClass != null)
          return ActionFactory.createAction(actionClass);
          
      }
      return null;
   }
   
}
