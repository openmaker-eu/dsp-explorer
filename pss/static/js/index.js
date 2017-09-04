/**
 * Created by alexcomu on 03/08/17.
 */
import * as angular from 'angular';

require("../style/index.scss")
let baseImports = require("../../../static/js/index")
require("./upload.behaviour")
baseImports.angularForm()

// Init Angular APP
var app = angular.module('pss', ['ui.bootstrap','toastr'])
    .config(['$interpolateProvider', function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    }])

baseImports.angularBase(app)