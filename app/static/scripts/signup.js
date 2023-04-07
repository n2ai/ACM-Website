"use strict"

$(document).ready(()=>{
    
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    const submitBtn = $('#submit-btn');
    submitBtn.attr('disabled', true);

    $('#password2').on('keyup', function () {
        const password = $('#password').val();
        const password2 = $(this).val();
        if (password !== password2) {
          $('#password-mismatch-msg').show(); // display message
          submitBtn.attr('disabled', true); // disable submit button
        } else {
          $('#password-mismatch-msg').hide(); // hide message
          submitBtn.attr('disabled', false); // enable submit button
        }
      });


    $('form').on('submit',(e)=>{
        
        e.preventDefault()
        const firstName = $('#firstname').val()
        const lastName = $('#lastName').val()
        const email = $('#email').val()
        const password = $('#password').val()
        console.log(csrf_token)
        fetch('/signup', {
            method:'POST',
            body:JSON.stringify({
                firstName:firstName,
                lastName:lastName,
                email:email,
                password:password,
                csrf_token: csrfToken // include the CSRF token in the request body
            }),
            headers:{
                "content-type":"application/json; charset=UTF-8",
                "X-CSRFToken": $('input[name=csrf_token]').val()
                
            }
            
        })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            console.log(data)
        })
    })

})


