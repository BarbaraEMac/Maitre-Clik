/** JS for the Mobile app **/

var MaitreMobile = new function() {
    this.inited    = false; // Stpid hack
    this.checkedin = false; // true iff User has checked in for current meal
    this.voted     = false; // true iff User has voted for the current meal

    // User obj for current user. 
    this.user = new function () {
        this.uuid      = ""; // Unique # to id User on Server
        this.lastName  = ""; // Last Name
        this.firstName = ""; // First name 
        this.email     = ""; // Email address
        this.img       = ""; // URL to img of User
    };
    
    // Views for the Mobile App
    this.currentView = $("#voteView");

    // Initializer -------------------------------------------------------------
    this.init = function( ) {
        // Exit early if we've done this already!
        if( this.inited ) { return; }
        
        this.inited = true; // Set flag so we don't do this twice.

        // Some mathy hacks to fill topPanel width
        var g = $("body").width();
        var h = 82; 
        var f = (g - h) /2;
        $("#voteViewBtn").width( (f+6) + "px" ); 
        $("#eatingViewBtn").width( (g-h-f+6) + "px" ); 

        $( "#voteView_slider" ).change( function() {
            $("#voteView_amount").html( $(this).val() + "/10" );
        });

        // Attach key up handlers
        $("#onboard_firstName").keyup( function() { $("#onboard_email").val( $(this).val() + "@kik.com" ) } );

        // Attach click handlers.
        $("#voteView_submit").click( function() { MaitreMobile.vote(); } );
        $("#profileView_submit").click( function() { MaitreMobile.updateUser(); } );

        $("#voteViewBtn").click(     function() { MaitreMobile.showVoteView(); } );
        $("#eatingViewBtn").click(   function() { MaitreMobile.showEatingView(); } );
        $("#profileViewBtn").click(  function() { MaitreMobile.showProfileView(); } );
        
        $(".clikOutBtn").click( function() { MaitreMobile.clikOut(); } );
        $(".onboardBtn").click( function() { $(this).parent().hide().next().show(); } );
        $("#onboardSubmit").click( function() { MaitreMobile.createUser(); } );

        // Init Clik handlers.
        clik.on('eaterList', function(data) {
            // Update the eater list html
            $("#eatingFeed").html( data.list );
        });

        clik.on('leave', function(data) {
            $("#"+ data).remove();
        });

        clik.on('newMeal', function(data) {
            MaitreMobile.reset();
            MaitreMobile.showVoteView();

            alert("A new meal has arrived. Come eat!");
        });

        clik.on('clikIn', function(data) {
            MaitreMobile.checkinUser();

            // Go to vote screen
            MaitreMobile.showVoteView();
        });
    };
    
    this.reset = function() {
        /* Set JS back to factory default.
          Called whenever a new meal arrives. */

        this.voted     = false;
        this.checkedin = false;

        // Clean up views
        $( "#voteView_vote" ).show().next().hide();
        $( ".eatingFeedElem" ).remove();
        $( "#voteView_slider" ).val('5');

        // Now, clik OUT
        clik.clikOut();
    };
    
    this.run = function( ) {
        /* Call this fcn to start running the App. */

        this.init(); // Initialize the app.
    };

    this.clikIn = function() {
        /* Join the conference. */

        //clik.clikIn();
    };

    this.clikOut = function() {
        /* Leave the conference */

        // clik.clikOut();
    };

    // View Functions ----------------------------------------------------------
    this.showOnboardView = function( ) {
        /* Show the "Onboard" View */

        $("#topPanel").hide();

        $("#onboardView").children().hide();
        $("#onboardView_first").show();
        
        this.toggleView( "#onboardView" );  
    };
    this.showVoteView = function() {
        /* Show the "Vote" View */

        if ( clik.connected ) {
            if ( this.user.firstName == "" ) {
                this.showOnboardView();
            } else {
                $("#topPanel").show();

                $("#voteView_title").html("Bon Appetit, " + this.user.firstName);
            
                this.toggleView( "#voteView" );  
            }
        } else {
            this.clikIn();
        }
    };
    this.showProfileView = function() {
        /* Show "Profile" View */

        this.toggleView( "#profileView" );  
    };
    this.showEatingView = function() {
        /* Show "Who's Eating" View */

        if( clik.connected ) {
            this.toggleView( "#eatingView" );  
        } else {
            this.clikIn();
        }
    };
    
    this.toggleView = function( selector ) {
        /* Toggle view from current view to selector's view.
           selector: string CSS selector */

        this.currentView.hide();
        $("#"+this.currentView.attr('id')+"Btn").attr('class', 'limeBtn panelBtn');

        this.currentView = $( selector );

        $("#"+this.currentView.attr('id')+"Btn").attr('class', 'lightBlueBtn panelBtn');
        this.currentView.show();
    };

    // Ajax Functions ----------------------------------------------------------
    this.checkinUser = function( ) {
        /* Checks in a User for a meal.
           1. Tells Clik.
           2. Tells server. 
        */

        if( this.user.firstName == "" ) { return; }
        if( this.checkedin == true ) { return; } // Only once per meal.
        
        this.checkedin = true; // Set flag.
    
        // Tell Clik!
        clik.send( 'checkin', { firstName : this.user.firstName,
                                uuid      : this.user.uuid,
                                img       : this.user.img,
                                clik_id   : clik.client.id } );

        // Tell server!
        $.ajax({ url     : "{% url CreateCheckin %}",
                 type    : "POST",
                 data    : ( { user_uuid : this.user.uuid } ),
                 success : function(response) {
                 }
           });
    };

    this.createUser = function( ) {
        /* Create a new User obj on the Server. */

        var firstName = $("#onboard_firstName").val();
        var lastName  = $("#onboard_lastName").val();
        var email     = $("#onboard_email").val();

        // Cache this stuff!
        this.user.firstName = firstName;
        this.user.lastName  = lastName;
        this.user.email     = email;

        // Update the profile page.
        $("#profileView_name").html( firstName + " " + lastName );
        $("#profileView_email").val( email );

         // Tell the Server to make a new User.
         $.ajax({
                url: "{% url CreateUser %}",
                type: "POST",
                data: ({ firstName : firstName,
                         lastName  : lastName,
                         email     : email } ),
                success: function(response) {
                    // Store User info for future use.
                    MaitreMobile.user.uuid  = response.uuid;
                    MaitreMobile.user.img   = response.img;
                    
                    MaitreMobile.checkinUser();
                    
                    // Go to Vote View.
                    MaitreMobile.showVoteView();
                },
            });
    };

    this.vote = function( vote ) {
        /* Assign a numerical value in range [1, 10] to the
           current meal. 1 = bad, 10 = best. */

        if ( this.voted == true ) { return; } // Vote once per meal
        
        this.voted = true; // Set the flag. No voting twice!

        var vote_val = $( "#voteView_slider" ).val();

        // Tell Clik Desktop about the vote
        clik.send( 'vote', { firstName  : this.user.firstName,
                             uuid       : this.user.uuid,
                             img        : this.user.img,
                             voteValue  : vote_val } );
        
        // Go to Thanks View on successful vote.
        $("#voteView_vote").hide().next().show();
        
        // Tell server
        $.ajax({ url: "{% url DoVote %}",
                 type: "POST",
                 data: ({ value : vote_val } ),
                 success: function(response) {
                 },
              });
    };

    this.updateUser = function() {
        /* Update the User's information on the server.
           Right now, you can only update:
           1. Email
           2. Notification email flag.
        */

        var email = $("#profileView_email").val();
        var yes   = $("#notif_yes").attr('checked') != undefined;

        // Tell server
        $.ajax({ url: "{% url UpdateUser %}",
                 type: "POST",
                 data: ({ email            : email,
                          notification_yes : yes } ),
                 success: function(response) {
                     $("#profileView_thanks").show();
                     setTimeout( function(){$("#profileView_thanks").hide();}, 3000 );

                     // Go to Thanks View on successful vote.
                     MaitreMobile.showProfileView();
                 },
              });
    };
};


// Let's run this thing when the DOM is ready!!
clik.on('ready', function() {
    MaitreMobile.init();
});
