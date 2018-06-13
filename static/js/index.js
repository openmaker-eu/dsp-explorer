//import 'babel-polyfill';
// Import jquery
var jQuery = window.$ = window.jQuery = require('jquery')
// Import angularjs
var angular = require('../../node_modules/angular/angular')
// Import Moment.js
import moment from '../../node_modules/moment/min/moment-with-locales';
window.moment = moment

// Import angular google maps
require('../../node_modules/ngmap')
// Import bootstrap sass
require("bootstrap-sass")
// Import cookie consent
require("../../node_modules/cookieconsent/build/cookieconsent.min"); // library
require("../../static/js/cookie/cookie.policy.behaviour"); // Config
// Import fontawesome 5
import fontawesome from '@fortawesome/fontawesome'
// Import lodash
import  * as  _  from 'lodash';

export function angularBase(app=null){
    // Import angular componenets
    app && app.factory('ModalFactory', require('./factories/modal.factory').default )
    app && app.factory('LoginService', require('./factories/LoginService').default )
    app && app.factory('MessageModal', require('./factories/message.modal.factory').default )
    app && app.directive('baseApp', require('./directives/BaseApp').default )
    return this
}

export function angularForm(app){
    
    require('angular-ui-bootstrap');
    require('angular-toastr');
    require('angular-sanitize');
    require('angular-animate');
    require("ui-select")
    return this
}

export function directives(app){
    app.component('circleImage', require('./directives/CircleImage').default )
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

