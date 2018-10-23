import * as _ from 'lodash'
let template =  require('./templates/ProfileDetailPage.html')

export default [function(){
    return {
        template:template,
        scope: {
            entityname: '@',
            entityid : '@',
            slider: '@'
        },
        controller : ['$scope', '$rootScope', '$http', 'EntityProvider', 'ContactUserModal' ,
            function($scope, $rootScope, $http, EntityProvider, ContactUserModal)
        {

            $scope.is_my_profile = false
            
            $rootScope.$watch('user', (n)=>$scope.is_my_profile = $scope.entityid && $scope.entityid == _.get(n, 'profile'))
            
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            $scope.entity = EntityProvider.make($scope.entityname,$scope.entityid)
            $scope.nodata = !$scope.entity.get()
    
            $scope.edit = ()=>
                $rootScope.$emit('question.modal.open', null, 'profileedit' )
            
            
            $scope.tooltip_template = "<i class='fas fa-user-edit'></i>&nbsp;&nbsp;Click to edit"
            
            $scope.openContactUserModal = ()=>ContactUserModal.open($scope.entity.data)
            

        }]
    }
}]



