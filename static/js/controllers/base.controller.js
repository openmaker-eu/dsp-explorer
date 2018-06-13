import * as _ from 'lodash'
export default
            ['$scope','$http','$rootScope','toastr','MessageModal','QuestionModal','LoginService',
    function ($scope, $http, $rootScope, toastr, MessageModal, QuestionModal, LoginService) {
    
    // GLOBAL ACTIONS
    $scope.open_signup = ($event)=> { $event.stopPropagation(); $rootScope.$emit('question.modal.open') }
    $scope.logout =()=>LoginService.logout()
    $scope.login =()=>$rootScope.$emit('question.modal.open', [
        {name:'login', type:'login', label:'Insert your credentials', apicall: '/api/v1.4/login/', emitevent:'authorization.refresh'},
        {name:'end', type:'success', label: 'Successful login', }
    ])

}]

