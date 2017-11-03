/**
 * Created by alexcomu on 03/08/17.
 */
import * as angular from 'angular';
import '../../../node_modules/ng-prettyjson/src/ng-prettyjson'

require("../style/index.scss")
let baseImports = require("../../../static/js/index")
baseImports.angularForm()

// Init Angular APP
var app = angular.module('chatbot', ['ui.bootstrap','toastr', 'ngSanitize', 'ngPrettyJson'])
    .config(['$interpolateProvider', function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    }])


baseImports.angularBase(app)

app.controller('chatbotController', require('./controllers/chatbot.controller').default )
