/**
 * Created by andreafspeziale on 11/04/17.
 */
window.$ = window.jQuery = require('jquery')

require("bootstrap-sass")
require("bootstrap-sass/assets/stylesheets/_bootstrap.scss")
require("../style/dashboard.scss")

import  * as  _  from 'lodash'

import * as angular from 'angular';

require('angular-ui-bootstrap');
require('angular-toastr');
require('angular-sanitize');

var app = angular.module('dashboard', ['ui.bootstrap', 'toastr' , 'ngSanitize'])
    .config(function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    });

export { app };
