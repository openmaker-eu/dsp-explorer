import * as _ from 'lodash'
import * as d3 from 'd3';

export default [function(){
 
    return {
        template:`<ng-transclude></ng-transclude>`,
        transclude:true,
        scope:{
            authorization:'=',
            user:'=',
            pageinfo:'='
        },
        controller : ['$scope', '$rootScope', '$http', 'LoginService', 'QuestionModal', function($scope, $rootScope, $http, LoginService, QuestionModal){
            
            // GLOBAL ACTIONS
            $rootScope.open_signup = ($event)=> { $event.stopPropagation(); $rootScope.$emit('question.modal.open') }
            $rootScope.logout =LoginService.logout
            $rootScope.login =()=>$rootScope.$emit('question.modal.open', [
                {name:'login', type:'login', label:'Insert your credentials', apicall: '/api/v1.4/login/', emitevent:'authorization.refresh'},
                {name:'end', type:'success', label: 'Successful login', }
            ])
            
            $rootScope.authorization=$scope.authorization
            $rootScope.user=$scope.user
            $rootScope.page_info=$scope.pageinfo
            
            console.log($scope.pageinfo);
            
        }]
    }
    
}]



