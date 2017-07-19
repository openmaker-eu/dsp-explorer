window.$ = window.jQuery = require('jquery')
window.m = window.moment = require("../../../node_modules/moment/moment")

require("bootstrap-sass")
require("../style/index.scss")
require('../../../node_modules/bootstrap-additions/dist/bootstrap-additions.min.css');

import  * as  _  from 'lodash'
import * as angular from 'angular';

require('angular-ui-bootstrap');
require('angular-toastr');
require('angular-sanitize');
require('angular-animate');
require('angular-strap');
require("../../../node_modules/cookieconsent/build/cookieconsent.min");
require("ui-select")
require('ng-infinite-scroll')
require("../../../node_modules/vsGoogleAutocomplete/dist/vs-google-autocomplete");

var app = angular.module('dashboard', ['ui.bootstrap', 'toastr', 'ui.select','ngSanitize', 'ngAnimate','mgcrea.ngStrap', 'infinite-scroll', 'vsGoogleAutocomplete'])
    .config(['$interpolateProvider', function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    }]);

app.config(['$qProvider', function ($qProvider) {
    $qProvider.errorOnUnhandledRejections(false);
}]);

// Require static angular componenets
require("../../../static/js/index").default(app)

require("../../../static/js/footer/header.footer.behaviour")

app.controller('dashboardController', require('./controllers/dashboard.controller').default )
app.controller('onboardingController', require('./controllers/onboarding.controller').default )
app.controller('themesController', require('./controllers/themes.controller').default )
app.controller('searchController', require('./controllers/searchmembers.controller').default )

require("../../../static/js/cookie/cookie.policy.behaviour");
