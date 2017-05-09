window.$ = window.jQuery = require('jquery')

require("bootstrap-sass")
require("bootstrap-sass/assets/stylesheets/_bootstrap.scss")
require("../style/dashboard.scss")
require("angular-toastr/dist/angular-toastr.css")

import  * as  _  from 'lodash'
import * as angular from 'angular';

require('angular-ui-bootstrap');
require('angular-toastr');
require('angular-sanitize');

let app = angular.module('dashboard', ['ui.bootstrap', 'toastr' , 'ngSanitize'])
    .config(['$interpolateProvider', function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    }]);

app.config(['$qProvider', function ($qProvider) {
    $qProvider.errorOnUnhandledRejections(false);
}]);

app.controller('baseController', require('../../../static/js/controllers/base.controller').default )

export { app };

app.controller('dashboardController', require('./controllers/dashboard.controller').default )
app.controller('searchController', require('./controllers/searchmembers.controller').default )

