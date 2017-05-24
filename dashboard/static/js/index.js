window.$ = window.jQuery = require('jquery')

require("bootstrap-sass")
require("bootstrap-sass/assets/stylesheets/_bootstrap.scss")
require("../style/dashboard.scss")
require("../style/card.scss")
require("angular-toastr/dist/angular-toastr.css")
require("../../../node_modules/cookieconsent/build/cookieconsent.min.css");
require("../../../node_modules/cookieconsent/build/cookieconsent.min");

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
require("../../../static/js/footer/footer")


export { app };

app.controller('dashboardController', require('./controllers/dashboard.controller').default )
app.controller('searchController', require('./controllers/searchmembers.controller').default )

require("../../../static/js/cookie/cookiePolicy");