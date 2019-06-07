$(document).ready(function () {
    // session = new QiSession("127.0.0.1:80");

    //  use qimessaging-json directly 
    // the port 8002 is the port qimessaging-json is listening to
    // the string "1.0" avoids to have to rewrite url with reverse proxy
    session = new QiSession("127.0.0.1:8002", "1.0");

    $('#page_empty').show();
    $('#page_1').hide();
    $('#page_2').hide();


    session.service("ALMemory").done(function(ALMemory) {

        ALMemory.subscriber("SimpleWeb/Page0").done(function(subscriber) {

            subscriber.signal.connect(function(val) {
                $('#page_empty').show();
                $('#page_1').hide();
                $('#page_2').hide();
		console.log("val:"+val);
		$('#text_start').html("<h1>"+val+"</h1>");
            });
        });


        ALMemory.subscriber("SimpleWeb/Page1").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_1').show();
                $('#page_empty').hide();
                $('#page_2').hide();

            });
        });


    });

    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }

    $('#footer_start').on('click', function() {
        console.log("click Start");
        raise('SimpleWeb/Start', 1)
    });

    $('#choice_1_1').on('click', function() {
        console.log("click 1");
        raise('SimpleWeb/Button1', 1);
    });

    $('#choice_1_2').on('click', function() {
        console.log("click 2");
        raise('SimpleWeb/Button2', 1);
    });

    $('#choice_1_3').on('click', function() {
        console.log("click 3");
        raise('SimpleWeb/Button3', 1);
    });
    $('#choice_1_4').on('click', function() {
        console.log("click 4");
        raise('SimpleWeb/Button4', 1);
    });
    $('#choice_1_5').on('click', function() {
        console.log("click 5");
        raise('SimpleWeb/Button5', 1);
    });
    $('#choice_1_6').on('click', function() {
        console.log("click 6");
        raise('SimpleWeb/Button6', 1);
    });


});
