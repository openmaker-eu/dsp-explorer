window.addEventListener("load", function(){
    window.cookieconsent.initialise({
        "palette": {
            "popup": {
                "background": "#e3e3e3",
                "text": "#fff"
            },
            "button": {
                "background": "transparent",
                "text": "#fff",
                "border": "#fff"
            }
        },
        "position": "bottom-right",
        "content": {
            "href": "/privacy",
            "message": "This site uses cookies, as explained in our Privacy Policy. If you use this site without adjusting your cookies settings, you agree to our use of cookies.\n",
            "dismiss": "Close!",
            "link": "Learn more"
        }
    })});