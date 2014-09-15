
var buildDropdown = function(priority, id){
	switch(priority){
	case 1:
		return '<select class="priority" id=' + id + '><option value="1" selected="true">High</option><option value="2">Normal</option><option value="3">Low</option></select>';
	case 2:
		return '<select class="priority" id=' + id + '><option value="1">High</option><option value="2" selected="true">Normal</option><option value="3">Low</option></select>';
	default:
		return '<select class="priority" id=' + id + '><option value="1">High</option><option value="2">Normal</option><option value="3" selected="true">Low</option></select>';
	}
}

var makeTodo = function(data){
	var checked = '';
	if (data["completed"] == true){
		checked = ' checked ';
		var text = '<td class="todoText" id=' + data['id'] + 
					'><span style="text-decoration:line-through;">' +  data['text']; + '</span></td>'
	} else {
		var text = '<td class="todoText" id=' + data['id'] +'><span>' +  data['text']; + '</span></td>'
	}
	

	var checkbox = '<td><input type=checkbox class="done" id=' + data['id'] + checked + '></td>';
	var close = '<td class="delete" id=' + data['id'] + '> X </td>';
	var priority =  '<td>' + buildDropdown(data['priority'], data['id']) + '</td>';
	
	var dueDate = '<td class="dateTd" id=' + data['id'] + '><input type="text" class="dueDate" value=""/></td>'
	if (data['due_date']){
		dueDate = '<td class="dateTd" id=' + data['id'] + '><input type="text" class="dueDate" value="' + 
					data['due_date'].substring(0, 10) + '" /></td>';
	}
	
    return '<tr class="item">' + checkbox + text + dueDate + priority + close + '</tr>' ;
}


var refreshList = function(){
	var sort = $('input[type=radio]:checked').val();
	var url = "/api/todo/?format=json&ordering=" + sort;

	if ($('input[name=showCompleted]').is(':checked') == false){
		url = url + "&completed=False"
	}
	
    $.get(url, function( data ) {
    	$('.item').remove();
        for (var i = 0; i < data.length; i++) {
            $( ".list" ).append(makeTodo(data[i]));
        }
        $(".dueDate").datepicker({ dateFormat: "yy-mm-dd" });
    });
}

var updateTodo = function(id){
	var text = $("#" + id + ".todoText > span").html();
	var priority = $("#" + id + ".priority").val();
	var dueDate = $("#" + id + ".dateTd > input").val();
    if (dueDate.length > 0){
    	dueDate = dueDate + "T00:00:00";
    }
	var checked = false;
	if ($("#" + id + ".done").attr("checked")){
		checked = true;
	}  
	$.ajax({
	    type: 'PUT',
	    url: '/api/todo/' + id,
	    data: {
	    	completed: checked,
	    	text: text,
	    	priority: priority,
	    	due_date: dueDate
	    	},
	    
	}).done(function() {
	    refreshList();
	});
}

$(document).ready(function() {

	$( "input[name=addDueDate]" ).datepicker({ dateFormat: "yy-mm-dd" });
	
	$('#add').click(function(){
        var todoText = $('input[name=addText]').val();
        if (todoText.length == 0){
        	return;
        }
        var todoPriority = $('select[name=addPriority]').val();
        var todoDueDate = $( "input[name=addDueDate]" ).val();
        if (todoDueDate.length > 0){
        	todoDueDate = todoDueDate + "T00:00:00";
        }
        $.ajax({
            type: 'POST',
            url: '/api/todo/',
            data: {
            	text: todoText,
            	priority: todoPriority,
            	due_date:todoDueDate,
            },
        }).done(function() {
	        $('input[name=addText]').val('');
	        $('select[name=addPriority]').val('2')
	        $("input[name=addDueDate]").val('');
	        refreshList();
        });
    });
    
    
    $('#refresh').click(function(){
    	refreshList();
    });
    
    $(document).on('click', '.delete', function() {
    	
    	if (false == confirm("Are you sure?")){
    		return;
    	}
    	
        var id = $(this).attr('id');
        $.ajax({
            type: 'DELETE',
            url: '/api/todo/' + id,
        }).done(function() {
	        refreshList();
        });
    });
    
    $(document).on('click', '.done', function() {
    	var id = $(this).attr('id');
    	updateTodo(id);
    });
    
    $("#list").on("change", ".priority", function () {
    	var id = $(this).attr('id');
    	updateTodo(id);
	});
    
    $("#list").on("change", ".dueDate", function () {
    	var id = $(this).parent().attr('id');
    	updateTodo(id);
	});
    
    $('input[type=radio]').change(function () {
    	refreshList();
	});
    
    $('input[name=showCompleted]').change(function () {
    	refreshList();
	});
    
    $(document).on("dblclick", ".todoText", function () {
    	var id = $(this).attr('id');
    	var oldText = $(this).children().html();
    	var newText = prompt("Change todo text",oldText);
    	if (newText) { 
    		$(this).children().html(newText);
    	}
    	updateTodo(id);
	});
    
    refreshList();
    
    
}); 