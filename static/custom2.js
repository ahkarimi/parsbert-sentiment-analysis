function submit_message(message) {
    $.post( "/send_message", {message: message}, handle_response);
    
    function handle_response(data) {
        // append the bot repsonse to the div
        $('.card-body').append(`
            <div class="d-flex justify-content-start mb-4">
    			<div class="img_cont_msg">
					<img src="/static/bot-icon.jpg" class="rounded-circle user_img_msg">
				</div>
    			<div class="msg_cotainer">
						${data.response}
    				<span class="msg_time">8:40 AM, Today</span>
				</div>
    		</div>
        `)
        
        // remove the loading indicator
        $( "#loading" ).remove();
    }
}

$('#target').on('submit', function(e){
    e.preventDefault();
    const input_message = $('#input_message').val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }

    $('.card-body').append(`
        <div class="d-flex justify-content-end mb-4">
			<div class="msg_cotainer_send">
				 ${input_message}
				<span class="msg_time_send">8:55 AM, Today</span>
			</div>
			<div class="img_cont_msg">
    			<img src="/static/user-icon.jpg" class="rounded-circle user_img_msg">
			</div>
		</div>
    `)

    // loading 
    $('.card-body').append(`
        <div class="d-flex justify-content-start mb-4"  id="loading">
    		<div class="img_cont_msg">
				<img src="/static/bot-icon.jpg" class="rounded-circle user_img_msg">
			</div>
    		<div class="msg_cotainer">
				<b>...</b>
    		<span class="msg_time">8:40 AM, Today</span>
			</div>
    	</div>
    `)

    // clear the text input 
    $('#input_message').val('')

    // send the message
    submit_message(input_message)
});




