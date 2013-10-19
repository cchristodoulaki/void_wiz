<%-- 
    Document   : index
    Created on : Jul 5, 2013, 12:22:59 PM
    Author     : christina

    University of Toronto, Database Group

# Author: Christina Christodoulakis
# 
#    Copyright 2013 Christina Christodoulakis
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>VoidWiz - Fill the Void </title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        
        <link rel="stylesheet" href="css/bootstrap.css">
        <link rel="stylesheet" href="css/font-awesome/css/font-awesome.min.css">
<!--        <link rel="stylesheet" href="css/bootstrap.min.css">  
        <link rel="stylesheet" href="css/bootstrap-responsive.min.css">-->
        <link rel="stylesheet" href="css/main.css">
        <script src="js/vendor/jquery-1.10.1.min.js"></script>
        
        <script src="./js/vendor/bootstrap.js"></script>
<!--        <script src="./js/vendor/bootstrap-tooltip.js"></script>
        <script src="./js/vendor/bootstrap-popover.js"></script>-->
        <script src="./js/d3.v3/d3.v3.js"></script>
        <!--<script src="./js/vendor/modernizr-2.6.2-respond-1.1.0.min.js"></script>-->
        
        <script src="./js/dvj.js"></script>
        <!--<script src="./js/main.js"></script>-->
            
    </head>
    
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->

        <!-- This code is taken from http://twitter.github.com/bootstrap/examples/hero.html -->
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </a>
                    <a class="brand" href="http://www.cs.utoronto.ca/~christina/apps/VoidWiz/index.jsp">VoidWiz</a>
                    <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="active"><a href="http://www.cs.utoronto.ca/~christina/apps/VoidWiz/index.jsp">Toy</a></li>
              <li><a href="http://www.cs.utoronto.ca/~christina/apps/VoidWiz/ct.jsp">Clinical Trials</a></li>
              <li><a href="http://graphics.tu-bs.de/static/teaching/seminars/ss13/CG/papers/Klose02.pdf">About BBP</a></li>
              
<!--              <li><a href="#contact">Contact</a></li>
              <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="#">Action</a></li>
                  <li><a href="#">Another action</a></li>
                  <li><a href="#">Something else here</a></li>
                  <li class="divider"></li>
                  <li class="nav-header">Nav header</li>
                  <li><a href="#">Separated link</a></li>
                  <li><a href="#">One more separated link</a></li>
                </ul>
              </li>-->
            </ul>
          </div><!--/.nav-collapse -->

                </div>
            </div>
        </div>

        <div class="container">
            <!-- Example row of columns -->
            <div class="row">
                <div class="span8">
                    <h2>Graph View</h2>
                    <p>Displaying <strong>Patient Visit</strong> as a hypergraph.</p>
                    <!--<p><a class="btn" href="#">Legend &raquo;</a></p>-->
                    <div id="graphViz"></div>
                </div>
                
                <div class="span3">
                    <h2>Tools</h2>
                    <p id="null_node"></p>
                    <p><a class="btn btn-info " href="javascript:retrieveBBP();">Run Belief Propagation &raquo;</a></p>
<!--                    <p><a class="btn" href="#">RWR (Random walks with restarts) &raquo;</a></p>
                    <p><a class="btn" href="#">View details &raquo;</a></p>-->
<div id="bbp_results"></div>
               </div>
            </div>

            <hr>
            <!-- Main hero unit for a primary marketing message or call to action -->
            <div class="hero-unit">
                <h2>Tabular View</h2>
                <div id="tuple_preview"></div>
            </div>
            <hr>

            <footer>
                <p>&copy; <a href="http://www.cs.utoronto.ca/~christina">Christina Christodoulakis</a>, <a href="http://web.cs.toronto.edu/">University of Toronto</a>, 2013 </p><embed src="img/uoftdb.svg" type="image/svg+xml" style="float:right;"/>
            </footer>

        </div> <!-- /container -->

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.10.1.min.js"><\/script>')</script>

        <script src="js/vendor/bootstrap.min.js"></script>
        <script src="js/main.js"></script>

</body>
</html>
