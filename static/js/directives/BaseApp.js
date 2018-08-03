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
        controller : ['$scope', '$rootScope', '$http', 'LoginService', 'QuestionModal', '$element',
            function($scope, $rootScope, $http, LoginService, QuestionModal, $element){
            
            // GLOBAL ACTIONS
            $rootScope.open_signup = ($event)=> { $event.stopPropagation(); $rootScope.$emit('question.modal.open') }
            $rootScope.logout =LoginService.logout
            
                $rootScope.login =()=>QuestionModal.open(
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
            
            $rootScope.authorization=$scope.authorization
            $rootScope.twitter_auth=$scope.twitterauth
            $rootScope.user=$scope.user
            $rootScope.page_info=$scope.pageinfo
            $rootScope.bookmarks=$scope.bookmarks
            $rootScope.$on('authorization.refresh', ()=>$scope.on_auth_refresh())
            $rootScope.twitter_auth && $rootScope.page_info.name === "homepage" && $rootScope.login()
            
            $scope.on_auth_refresh = ()=>{
                let nav = $('.navbar-collapse')
                nav.collapse('hide')
            }
            
            
        }]
    }
    
}]



