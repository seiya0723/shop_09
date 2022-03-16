window.addEventListener("load" , function (){

    $("#submit").on("click", function(){ submit(); });

    $(document).on("click", ".trash", function(){ trash(this); })

    //下記はコメント投稿後、通用しない。上記のやり方であれば通用する。
    //$(".trash").on("click", function(){ trash(this); });

});


function submit(){

    let form_elem   = "#form_area";

    let data    = new FormData( $(form_elem).get(0) );
    let url     = $(form_elem).prop("action");
    let method  = $(form_elem).prop("method");

    for (let v of data ){ console.log(v); }

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 

        if (data.error){
            console.log("ERROR");
        }
        else{
            $("#content_area").html(data.content);
            $("#textarea").val("");
        }

    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}

function trash(elem){

    let form_elem   = $(elem).parent("form");
    let url         = $(form_elem).prop("action");

    $.ajax({
        url: url,
        type: "DELETE",
        data: { "test":"aaaa","test2":"bbb" },
        dataType: 'json'
    }).done( function(data, status, xhr ) { 
        console.log(data);
    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    }); 

}

