"use strict"

$(document).ready(()=>{
    

    $('form').on('submit',(e)=>{
        
        e.preventDefault()
        const firstName = $('#firstname').val()
        const lastName = $('#lastName').val()
        const email = $('#email').val()
        const password = $('#password').val()
        fetch('https://jsonplaceholder.typicode.com/posts', {
            method:'POST',
            body:JSON.stringify({
                firstName:firstName,
                lastName:lastName,
                email:email,
                password:password
            }),
            headers:{
                "content-type":"application/json; charset=UTF-8"
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


