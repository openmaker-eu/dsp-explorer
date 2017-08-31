// Import Js library
window.$ = window.jQuery = require('jquery')
window.m = window.moment = require("../../node_modules/moment/moment")

// Import bootstrap sass
require("bootstrap-sass")

// Import cookie consent
require("../../node_modules/cookieconsent/build/cookieconsent.min"); // library
require("../../static/js/cookie/cookie.policy.behaviour"); // Config
import  * as  _  from 'lodash'

export function angularBase(app=null){
    
    // Import angular componenets
    app && app.factory('ModalFactory', require('./factories/modal.factory').default )
    app && app.factory('MessageModal', require('./factories/message.modal.factory').default )
    app && app.controller('baseController', require('./controllers/base.controller').default )
    return this
}

export function angularForm(){
    
    require('angular-ui-bootstrap');
    require('angular-toastr');
    require('angular-sanitize');
    require('angular-animate');
    require('angular-strap');
    require("ui-select")
    return this
}
