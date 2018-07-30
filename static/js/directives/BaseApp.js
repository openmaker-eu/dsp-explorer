import * as _ from 'lodash'
import * as d3 from 'd3';

export default [function(){
 
    return {
        template:`<ng-transclude></ng-transclude>`,
        transclude:true,
        scope:{
            authorization:'=',
            twitterauth:'=',
            user:'=',
            bookmarks:'=',
            pageinfo:'='
        },
        controller : ['$scope', '$rootScope', '$http', 'LoginService', 'QuestionModal', function($scope, $rootScope, $http, LoginService, QuestionModal){
            
            // GLOBAL ACTIONS
            $rootScope.open_signup = ($event)=> { $event.stopPropagation(); $rootScope.$emit('question.modal.open') }
            $rootScope.logout =LoginService.logout
            $rootScope.login =()=>$rootScope.$emit('question.modal.open', [
                {
                    name:'login',
                    type:'login',
                    label:'Login',
                    apicall: '/api/v1.4/login/',
                    emitevent:'authorization.refresh',
                    custom_next:`<h4>LOGIN&nbsp;&nbsp;</h4>`
                },
                {name:'end', type:'success', label: 'Successful login', custom_prev:null }
            ])
            
            $rootScope.authorization=$scope.authorization
            $rootScope.twitter_auth=$scope.twitterauth
            $rootScope.user=$scope.user
            $rootScope.page_info=$scope.pageinfo
            $rootScope.bookmarks=$scope.bookmarks
    
            $rootScope.$on('authorization.refresh', ()=>console.log('main auth refresh'))
            console.log('bookmarks', $rootScope.bookmarks);
            $rootScope.twitter_auth && $rootScope.page_info.name === "homepage" && $rootScope.login()
            
            
            
        }]
    }
    
}]



