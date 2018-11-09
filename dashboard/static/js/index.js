//Require static angular componenets
let baseImports = require("../../../static/js/index")

require('../../../node_modules/angular-moment-picker/dist/angular-moment-picker')
require('../../../node_modules/angular-cookies')
require("../style/index.scss")

// Angular form imports
baseImports.angularForm()

// Stuff
require("../../../node_modules/vsGoogleAutocomplete/dist/vs-google-autocomplete");
require("../../../node_modules/vsGoogleAutocomplete/dist/vs-autocomplete-validator");

import slickCarousel from 'slick-carousel';
require("../../../node_modules/slick-carousel/slick/slick.css");
require("../../../node_modules/slick-carousel/slick/slick-theme.css");
require("../../../node_modules/slick-carousel");
require("../../../node_modules/angular-slick-carousel/");
require("../../../node_modules/angular-hammer");
require("../../../node_modules/chart.js/dist/Chart.bundle.js");
require("../../../node_modules/angular-chart.js");
require('../../../node_modules/ngmap');
require('../../../node_modules/angular-recaptcha');


// Init Angular APP
var app = angular.module('dashboard', [
    'ui.bootstrap',
    'toastr',
    'ui.select',
    'ngSanitize',
    'ngAnimate',
    'vsGoogleAutocomplete',
    'ngMap',
    'slickCarousel',
    'moment-picker',
    'ngCookies',
    'hmTouchEvents',
    'chart.js',
    'vcRecaptcha'
])
    .config(['$interpolateProvider', function($interpolateProvider) {
            $interpolateProvider.startSymbol('{$');
            $interpolateProvider.endSymbol('$}');
    }])
    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])
    .config(['$qProvider', function ($qProvider) {$qProvider.errorOnUnhandledRejections(false);}])
;


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

// Challenge
app.directive('challengeList', require('./directives/challenge/ChallengeList').default )
app.directive('challenge', require('./directives/challenge/Challenge').default )

// Projects
app.directive('projectDetail', require('./directives/project/ProjectDetail').default )
app.directive('projectList', require('./directives/project/ProjectList').default )
app.directive('project', require('./directives/project/Project').default )

/******
* MDP *
*******/

// Pages
app.directive('homePage', require('./directives/pages/HomePage').default )
app.directive('entityListPage', require('./directives/pages/EntityListPage').default )
app.directive('entityDetailPage', require('./directives/pages/EntityDetailPage').default )
app.directive('profileDetailPage', require('./directives/pages/ProfileDetailPage').default )

// Page Blocks
app.directive('entityCarousel', require('./directives/entity/EntityCarousel').default )
app.directive('entitySidebar', require('./directives/entity/EntitySidebar').default )
app.directive('entityDetail', require('./directives/entity/EntityDetail').default )
app.directive('bookmarkedStripe', require('./directives/entity/BookmarkedStripe').default )
app.directive('userProjectsStripe', require('./directives/entity/UserProjectsStripe').default )
app.directive('entityInterested', require('./directives/entity/EntityInterested').default )

// Dynamic Elements
app.factory('QuestionModal', require('./factories/QuestionModal').default )

// Page small elements (partials)
app.directive('bookmarkedStripeToggler', require('./directives/partials/BookmarkedStripeToggler').default )
app.directive('bookmarkButton', require('./directives/partials/BookmarkButton').default )
app.directive('interestButton', require('./directives/partials/InterestButton').default )
app.directive('entityLoading', require('./directives/partials/EtityLoading').default )
app.directive('accountDelete', require('./directives/partials/AccountDelete').default )
app.directive('entityDelete', require('./directives/entity/EntityDelete').default )

// Questions/Chatbot
app.directive('wizard', require('./directives/questions/Wizard').default )
app.component('question', require('./directives/questions/Question').default )
app.directive('chatbot', require('./directives/questions/Chatbot').default )
app.directive('profileQuestions', require('./directives/questions/ProfileQuestions').default )

app.directive('naviQuestions', require('./directives/questions/NaviQuestions').default )
app.directive('naviChatbot', require('./directives/questions/NaviChatbot').default )

app.component('activityQuestion', require('./directives/questions/ActivityQuestion').default )

// Factories
app.factory('ContactUserModal', require('./factories/ContactUserWithEmailModal').default )

// Content providers
app.factory('EntityProvider', require('./content_providers/EntityProvider').default )

//Community Stats
app.directive('genderGraph', require('./directives/graphs/genderGraph').default )
app.directive('ageGraph', require('./directives/graphs/ageGraph').default)
app.directive('jobGraph', require('./directives/graphs/jobGraph').default)
app.directive('cityGraph', require('./directives/graphs/cityGraph').default)