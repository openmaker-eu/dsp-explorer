window.$ = window.jQuery = require('jquery')

require("bootstrap-sass")
require("bootstrap-sass/assets/stylesheets/_bootstrap.scss")
require("../style/dashboard.scss")

import  * as  _  from 'lodash'

import * as angular from 'angular';

require('angular-ui-bootstrap');
require('angular-toastr');
require('angular-sanitize');

let app = angular.module('dashboard', ['ui.bootstrap', 'toastr' , 'ngSanitize'])
    .config(function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    });

app.controller('baseController', require('../../../static/js/controllers/base.controller').default )

export { app };

app.controller('dashboardController', require('./controllers/dashboard.controller').default )

