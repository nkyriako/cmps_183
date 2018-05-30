// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    // Enumerates an array. 
    var enumerate = function(v) {
        var k=0;
        return v.map(function(e) {e._idx = k++;});
    };

    self.get_user_email = function(){
        $.getJSON(
            get_user_email_url,
	    function(data) {
		self.vue.user_email = data.email;
            }
        );
    }

    // GET FORUM DATA
    self.get_forum = function(){
        //console.log("in get_forum");
	$.getJSON(
	    get_forum_url,
	    function (data) {
		self.vue.forum = data.forum;
		enumerate(self.vue.forum);
   	    }
	);
    };

    // ADD A NEW POST
    self.add_track = function(){
        $.post(add_track_url,
            {
                title: self.vue.form_title,
                memo: self.vue.form_memo,
            },
            function (data) {
                //$.web2py.enableElement($("#add_track_submit"));
                console.log(self.vue.user_email);
		let obj={title:self.vue.form_title,memo:self.vue.form_memo, email:self.vue.user_email}	
                self.vue.forum.unshift(obj);
                //self.get_forum();
            }
        );
        //setTimeout(function(){ 
            //alert('hello');
            //self.get_forum();
        //}, 3000);
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            forum: [],
            form_title: "",
            form_memo: "",
            logged_in: false,
            user_email: ""
        },
        methods: {
            get_forum: self.get_forum,
            add_track: self.add_track,
        }

    });

    self.get_user_email();
    self.get_forum();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
