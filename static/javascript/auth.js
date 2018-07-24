$(function(){
	var authForm = $('#authForm')
	var url = "http://127.0.0.1:8080/auth"
	authForm.on("submit", function(e){
		e.preventDefault();
		$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify(translateToJSON($('#authForm')))
		})
		.done(function(res){
			console.log(res)
		})
	});

	function translateToJSON($form){
 		var unindexedArray = $form.serializeArray();
 		var indexedArray = {};
 		$.map(unindexedArray, function(index, elem) {
 			indexedArray[index['name']] = index['value'];
	
 		});
 		return indexedArray;
 	}
})