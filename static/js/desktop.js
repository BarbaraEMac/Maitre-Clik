/** JS for the Desktop app **/

// Common JS fcns.
Array.prototype.has=function(v){
    for (i=0; i<this.length; i++){
        if (this[i]==v) return true;
    }
    return false;
}

var MaitreDesktop = new function() {
    /* MaitreDesktop
       A Clik application to track people while they eat
       their meals at Kik.
    */

    // The view that is curently being displayed
    this.currentView = $("#mainView");
    
    this.checkedin   = []; // List of uuids for people who checked in.
    this.voters      = []; // List of uuids for people who have already voted.
    
    // A 'vote' struct to keep track of the votes for current meal
    this.votes     = new function() 
        {
            this.sum      = 0;  // Sum total of the votes
            this.numVotes = 0;  // Number of votes cast

            this.percent = function() {
                // Returns an Int of the percentage of votes for current meal
                if ( this.numVotes == 0 ) { return 0; }

                return Math.round( 10 * (this.sum / this.numVotes) );
            };
        };

    // Initializer -------------------------------------------------------------
    this.init = function( ) {
        /* Initialize the App. */

        // Init Views 
        $("#statsViewBtn").click(    function() { MaitreDesktop.showStatsView(); } );
        $("#mainViewBtn").click(     function() { MaitreDesktop.showMainView(); } );
        $("#feedViewBtn").click(     function() { MaitreDesktop.showEatingView(); } );
        $("#newMealView_Btn").click( function() { MaitreDesktop.showNewMealView(); } );
        $("#newMealSubmit").click(   function() { MaitreDesktop.submitMeal(); } );
        $("#newMealCancel").click(   function() { MaitreDesktop.showMainView(); } );

        // Set to factory default
        this.reset();
        // Start Timer to display 'New Meal' button for caterer at 10am and 4pm daily.
        this.newMealBtnTimer();

        // Start timers for a) wait for clik URL b) wait for clik overlay
        setTimeout( function() { MaitreDesktop.waitForURL(); }, 300 );
        setTimeout( function() { MaitreDesktop.removeClikOverlay(); }, 300 );

        // Init clik event handlers
        clik.on('checkin', function ( data ) {
            
            if ( MaitreDesktop.checkedin.has( data.uuid ) ) { return; }

            // Append User's uuid to checked-in list.
            MaitreDesktop.checkedin.push( data.uuid );

            // Update event feed
            var msg = data.firstName + " is eating.";
            MaitreDesktop.addToFeed( msg, data.img );

            // Add User's info to eater list.
            var li = $( document.createElement( 'li' ) );
            li.attr( 'id', data.clik_id );
            li.attr( 'class', 'eatingListElem' );
            li.html( '<p>' + data.firstName + '</p>' );

            li.insertBefore( "#eatingList :first" );

            // Give ALL Users the list of people eating.
            clik.send( 'eaterList', { list : $("#eatingList").html() } );
        });

        clik.on('vote', function ( data ) {
            // Only let eaters vote ONCE per meal.
            if ( MaitreDesktop.voters.has( data.uuid ) ) { return; }

            // Append User's uuid to voter list.
            MaitreDesktop.voters.push( data.uuid );
            
            // Update feed.
            var text = "" + data.firstName + " voted! " + data.voteValue + "/10!!";
            MaitreDesktop.addToFeed( text, data.img );

            // Increment votes
            MaitreDesktop.votes.sum      += parseInt( data.voteValue );
            MaitreDesktop.votes.numVotes += 1;

            // Update UI.
            var per = MaitreDesktop.votes.percent();
            $("#mainView_barContainer").show();
            $("#mainView_yes").width("" + per + "%" );
            $("#mainView_yes").html("" + per + "%" );
        });
        
        // A user has left the conference
        clik.on('leave', function (data) {
            var msg = "Someone has left the building.";
            MaitreDesktop.addToFeed( msg, '/static/imgs/cliklogo.jpg' );

            $("#"+ data).remove();
        });
    };

    this.run = function( ) {
        /* The main fcn to run the application. 
           Call this when you're ready to start! */

        // Initialize the app.
        this.init();
    };

    this.reset = function() {
        /* Reset the votes for the next meal. */
        this.checkedin      = [];
        this.voters         = [];
        this.votes.sum      = 0;
        this.votes.numVotes = 0;

        $("#mainView_barContainer").hide();
        $("#newMealView_Btn").hide();

        $("#instructions").html( "Welcome Kik! Please Clik-In before grabbing your food!" );

        this.showMainView();
    };

    this.removeClikOverlay = function() {
        /* When Clik loads, it triggers an overlay to display by default.
           I don't want this to show, so let's remove it when it's in the 
           DOM. */

        var el = $("#clik-paper"); 
        
        if( el != undefined ) {
            el.remove();
        } else {
            setTimeout( function() { MaitreDesktop.removeClikOverlay(); }, 300 );
        }
    };

    this.addToFeed = function( msg, img ) {
        /* Given an input string representing a new status,
           update the status msg divs contents. */
        var li = $( document.createElement( 'li' ) );

        var img = "<img src='" + img + "' />";
        var p   = "<p>" + msg + "</p>";
        li.html( img + p);
        
        li.insertBefore( "#mainFeed :first" );
    };

    this.waitForURL = function() {
        /* clik.clikCodeURL() takes awhile to become not undefined.
           Let's spin and wait for it to load. */

        var url = clik.clikCodeURL();

        if ( url == undefined ) {
            setTimeout( function(){ MaitreDesktop.waitForURL(); }, 300 );
        } else {
            $("#qrContainer").attr( 'src', url );
        }
    };
    
    this.newMealBtnTimer = function() {
        /* Display the 'New Meal' button at 10am and 4pm for the caterer. */

        var now = new Date();
        var millisTill10 = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 10, 0, 0, 0) - now;
        if (millisTill10 < 0) {
             millisTill10 += 86400000; // it's after 10am, try 10am tomorrow.
        }
        var millisTill16 = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 16, 0, 0, 0) - now;
        if (millisTill16 < 0) {
             millisTill16 += 86400000; // it's after 4pm, try 4pm tomorrow.
        }
        setTimeout( function(){ MaitreDesktop.showNewMealBtn(); }, Math.min(millisTill10, millisTill16) );
    };


    // View Toggles ------------------------------------------------
    this.toggleView = function( selector ) {
        /* Toggle view from current view to selector's view.
           selector: string CSS selector */

        this.currentView.hide();
        $("#"+this.currentView.attr('id')+"Btn").attr('class', 'limeBtn');

        this.currentView = $( selector );

        $("#"+this.currentView.attr('id')+"Btn").attr('class', 'lightBlueBtn');
        this.currentView.fadeIn();
    };
    this.showStatsView = function() {
        /* Show 'Statistics' View */

        this.fetchStats();

        this.toggleView( "#statsView" );                  
    };
    this.showMainView = function() {
        /* Show 'Main' View */

        this.toggleView("#mainView");
        
        $("#navButtons").show();
        $("#rightSide").show();
    };
    this.showEatingView = function() {
        /* Show 'Feed' View */

        this.toggleView("#feedView");
    };
    this.showNewMealView = function() {
        /* Show 'New Meal' View */
        
        $("#newMealText").val("");
        $("#newMealText").show("");
        $("#newMealThanks").hide("");
        $("#newMealError").hide("");
        $("#newMealCancel").show();
        $("#newMealSubmit").show();

        $("#navButtons").hide();
        
        $("#rightSide").hide();
        
        this.toggleView("#newMealView");
    };
    this.showNewMealBtn = function() {
        /* Display the 'New Meal' button on the Main View */

        $("#instructions").html( "Welcome Wildcraft! After you've finished setting up the meal, please press 'New Meal' to notify everyone at Kik!" );

        $("#newMealView_Btn").show();
    };

    
    // Ajax Functions ----------------------------------------------------------
    this.fetchStats = function( ) {
        /* Grab the most recent stats obj from the server. */

         $.ajax({
                url: "{% url FetchStats %}",
                type: "GET",
                data: ( { } ),
                success: function(response) {
                },
            });
    };

    this.submitMeal = function( ) {
        /* Give the server details about this meal & 
           fire off emails to eaters! */
        
        var textElem = $("#newMealText");
        var menu     = textElem.val().trim();

        if ( menu.length == 0 ) {
            $("#newMealError").fadeIn();
        } else {
            $("#newMealError").hide();
            $("#newMealThanks").fadeIn();

            textElem.hide();
            $("#newMealCancel").hide();
            $("#newMealSubmit").hide();

            $("#mainView_menu").html( menu );

            // Update title
            var date = new Date();
            var type = '';
            if( date.getHours() >= 16 ) { type = 'Dinner'; } 
            else { type = 'Lunch'; }
            $("#mainView_subtitle").html( type + " Menu" );

            this.addToFeed( 'New meal! Thanks Wildcraft!', '/static/imgs/cliklogo.jpg' );

            // Tell anyone currently cliked-in.
            clik.send( 'newMeal', { } );
            
            setTimeout( function() { MaitreDesktop.reset(); }, 3500 );

            // Tell the server.
            $.ajax({
                    url: "{% url CreateMeal %}",
                    type: "POST",
                    data: ( { menu   : menu,
                              type   : type,
                              rating : this.votes.percent() } ),
                    success: function(response) {
                        return;
                    },
                });
        }
    };
};

// Let's run this thing when the DOM is ready!!
clik.on('ready', function() {
    MaitreDesktop.run();
});

