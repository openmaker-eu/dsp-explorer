import * as angular from 'angular';
require('../../../node_modules/ngmap')

// Import this app style
require("../style/index.scss")
// Require static angular componenets
let baseImports = require("../../../static/js/index")
// Angular form imports
baseImports.angularForm()

// Stuff
require('ng-infinite-scroll')
require("../../../node_modules/vsGoogleAutocomplete/dist/vs-google-autocomplete");
require("../../../node_modules/vsGoogleAutocomplete/dist/vs-autocomplete-validator");

// Init Angular APP
var app = angular.module('dashboard', [
    'ui.bootstrap', 'toastr', 'ui.select','ngSanitize', 'ngAnimate','mgcrea.ngStrap', 'infinite-scroll', 'vsGoogleAutocomplete', 'ngMap'
])
    .config(['$interpolateProvider', function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    }])
    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])
    .config(['$qProvider', function ($qProvider) {$qProvider.errorOnUnhandledRejections(false);}]);

// Require base angular componenets
baseImports.angularBase(app)
    .directives(app)
    .dataVizDirectives(app)


app.factory('UserSearchFactory', require('./factories/UserSearchFactory').default )
app.controller('landingController', require('./controllers/landing.controller').default )
app.controller('dashboardController', require('./controllers/dashboard.controller').default )
app.controller('insightController', require('./controllers/insight.controller').default )
app.controller('onboardingController', require('./controllers/onboarding.controller').default )
app.controller('themesController', require('./controllers/themes.controller').default )
app.controller('eventsController', require('./controllers/events.controller').default )
app.controller('searchController', require('./controllers/searchmembers.controller').default )
app.directive('userStories', require('./directives/UserStories.directive').default )
app.directive('challengeList', require('../../../static/js/directives/ChallengeList').default )


