export default [function(){
    return {
        template:`
            <span ng-click="toggle()">
                <i ng-if="!is_visible" class="glyphicon glyphicon-chevron-down text-red"></i>
                <i ng-if="is_visible" class="glyphicon glyphicon-chevron-up text-red"></i>
            </span>
        `,
        scope: {
            entityname : '@'
        },
        controller : ['$scope', '$rootScope',function($scope, $rootScope){
            
            $scope.is_visible = false;
            let event_name = 'bookmarked.'+$scope.entityname+'.visibility'
            
            $scope.toggle = ()=>{
                $scope.is_visible = !$scope.is_visible
                $rootScope.emit(event_name, {visible:$scope.is_visible})
            }
            
        }]
    }
}]
