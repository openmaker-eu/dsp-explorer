import * as _ from 'lodash'
import * as d3 from 'd3';

export default [function(){
    return {
        template:`<ng-transclude style="z-index:5000;"></ng-transclude>`,
        transclude:true,
        scope:{
            authorization:'=',
            twitterauth:'=',
            user:'=',
            bookmarks:'=',
            pageinfo:'=',
            twitterscreenname : '='
        },
        controller : ['$scope', '$rootScope', '$http', 'LoginService', 'QuestionModal', '$element', '$timeout', '$location', '$window',
            function($scope, $rootScope, $http, LoginService, QuestionModal, $element, $timeout, $location, $window){
            
            // GLOBAL ACTIONS
            $rootScope.open_signup = ($event)=> { $event.stopPropagation(); $rootScope.$emit('question.modal.open') }
            $rootScope.logout = LoginService.logout
            
            $rootScope.login =(oauth)=>{
                let timeout = oauth? 1000: 0
                $timeout(function(a){
                    QuestionModal.open(
                        null,
                        [
                            {
                                name:'login',
                                type:'login',
                                apicall: '/api/v1.4/login/',
                                emitevent:'authorization.refresh',
                                custom_next:`<h4>LOGIN&nbsp;&nbsp;</h4>`
                            },
                            {name:'end', type:'success', label: 'Successful login', custom_prev:null }
                        ]
                        ,'login'
                    )
                }, timeout)
            }
            
            $rootScope.alert_message = (message_type, message_text)=>{
                $rootScope.message = {type:message_type, text:message_text}
                let message_id = $rootScope.message.id = new Date().getUTCMilliseconds()
                $window.scrollTo(0,0)
                
                $timeout(function () {
                    $rootScope.message && $rootScope.message.id === message_id && ($rootScope.message=null)
                }, 20000)
                
            }
            
            
            $rootScope.authorization=$scope.authorization
            $rootScope.twitter_auth=$scope.twitterauth
            $rootScope.user=$scope.user
            $rootScope.page_info=$scope.pageinfo
            $rootScope.bookmarks=$scope.bookmarks
            
            $rootScope.$on('authorization.refresh', ()=>$scope.on_auth_refresh())
            $rootScope.twitter_auth && $rootScope.page_info.name === "homepage" && $rootScope.login('oauth')
            
            $scope.on_auth_refresh = ()=>{
                let nav = $('.navbar-collapse')
                nav.collapse('hide')
            }
    
            // Wait for elements to be rendered
            angular.element(()=>{
                // Open signup modal if url contains hash: #signup
                $timeout(function(a){
                    $location.hash() == 'signup' && $rootScope.$emit('question.modal.open')
                }, 1000)
            });

        }]
    }
    
}]



