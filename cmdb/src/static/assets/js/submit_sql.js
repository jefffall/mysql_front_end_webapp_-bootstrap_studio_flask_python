$(document).ready(function() {
    $("#submit_sql_query").click(function(event) {
        event.preventDefault();  
        
        $("#sql_output").html("<h3>WORKING...</h3><p><h3>Please wait!</h3>");
   
          var query = $('#sql_query_text').val();
        
         $.ajax({
			type: 'POST',
			url: "do_sql_query",
             data: JSON.stringify("sql_string" + ":" + query),
			//data: JSON.stringify("sql_string" + ":" + query),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
             
             success: function(response){
       
                 $("#sql_output").html(response.data);
            },
             error: function (response) {
         //$("#sql_output").html(response.statusText);
         $("#sql_output").html(response.data);
         ("#sql_output").html(response);

    }
		});
     });      
 });
      