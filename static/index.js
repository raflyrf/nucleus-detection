window.onload = () => {
	$('#sendbutton').click(() => {
		imagebox = $('#imagebox')
		input = $('#imageinput')[0]
		var tValuee = document.getElementById('tValue').value;
		//var value = e.value;
		//var text = e.options[e.selectedIndex].text;
		if(input.files && input.files[0])
		{
			var formData = new FormData();
			formData.append('image' , input.files[0]);
			formData.append('threshh' , tValuee);
			
			$.ajax({
				url: '/detectObject', // fix this to your GCE EXTERNAL IP
				type:'POST',
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log('upload error' , data);
					console.log(data.getAllResponseHeaders());
				},
				success: function(data){
					console.log(data);
					bytestring = data['status']
					image = bytestring.split('\'')[1]
					imagebox.attr('src' , 'data:image/jpeg;base64,'+image)
				}
			});
		}
	});
};



function readUrl(input){
	imagebox = $('#imagebox')
	console.log("evoked readUrl")
	if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
			// console.log(e)
			
			imagebox.attr('src',e.target.result); 
			imagebox.height(1080);
			imagebox.width(1080);
		}
		reader.readAsDataURL(input.files[0]);
	}

	
}