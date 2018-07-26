export default function(){
    return {
        template:`
            <span ng-if="$root.authorization >= 10" ng-click="toggle()">
                <i ng-if="!is_visible" class="fas fa-chevron-down text-red pointer"></i>
                <i ng-if="is_visible" class="fas fa-chevron-up text-red pointer"></i>
            </span>
        `,
        scope: {
            entityname : '@'
        },
        controller : ['$scope', '$rootScope',function($scope, $rootScope){
            
            $scope.is_visible = false;
            $scope.event_name = 'bookmarked.'+$scope.entityname+'.visibility'
            
            $scope.toggle = ()=>{
                $scope.is_visible = !$scope.is_visible
                $rootScope.$emit('bookmarked.'+$scope.entityname+'.visibility', {visible:$scope.is_visible})
            }
    
            // React to bookmark action
            $rootScope.$on('bookmarked.'+$scope.entityname+'.visibility', (e, m)=>{ $scope.is_visible=m.visible })
            
        }]
    }
}
