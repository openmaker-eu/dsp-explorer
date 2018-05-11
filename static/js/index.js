// Import Js library
window.$ = window.jQuery = require('jquery')
window.m = window.moment = require("../../node_modules/moment/moment")
import  * as  _  from 'lodash'

// Import bootstrap sass
require("bootstrap-sass")

// Import cookie consent
require("../../node_modules/cookieconsent/build/cookieconsent.min"); // library
require("../../static/js/cookie/cookie.policy.behaviour"); // Config

import fontawesome from '@fortawesome/fontawesome'


export function angularBase(app=null){
    
    // Import angular componenets
    app && app.factory('ModalFactory', require('./factories/modal.factory').default )
    app && app.factory('LoginService', require('./factories/LoginService').default )
    app && app.factory('MessageModal', require('./factories/message.modal.factory').default )
    app && app.controller('baseController', require('./controllers/base.controller').default )
    return this
}

export function angularForm(app){
    
    require('angular-ui-bootstrap');
    require('angular-toastr');
    require('angular-sanitize');
    require('angular-animate');
    require('angular-strap');
    require("ui-select")
    return this
}

export function directives(app){
    app.directive('circleImage', require('./directives/CircleImage').default )
    app.directive('inputFileModel', require('./directives/FileInputChange').default )
    return this
}

export function dataVizDirectives(app){
    app.directive('tagBubbles', require('./directives/TagBubbles').default )
    app.directive('pieSector', require('./directives/PieSector').default )
    app.directive('locationsMap', require('./directives/LocationsMap').default )
    app.directive('simplePagination', require('./directives/SimplePagination').default )
    return this
}
