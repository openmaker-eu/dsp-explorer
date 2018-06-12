export default function(){
    return {
        template:`
            <div ng-if="action='chatbot.question.simple'" style="display: flex; flex-direction:row; justify-content: center; padding-bottom:3%;">
                <div ng-repeat="act in items[current].actions.options" style="padding:1%;">
                    <button class="btn btn-danger pull-left" ng-click="next(act.value || act.label)">{$ act.label $}</button>
                </div>
            </div>
        `,
        scope: {
            items:'=',
            wizardid:'='
        },
        controller : ['$scope','$rootScope', function($scope, $rootScope){
            
            $scope.wizard_name = 'wizard.'+$scope.wizardid
            $scope.is_end = false
            $scope.current = 0;
            
            $scope.prev=()=>$rootScope.$emit($scope.wizard_name+'.prev', $scope.current)
            $scope.next=(value)=> {
                $scope.items[$scope.current].feedback = value
                $rootScope.$emit($scope.wizard_name+'.next', $scope.current)
                $scope.is_end && $scope.end()
            }
            
            $scope.end=()=>$rootScope.$emit($scope.wizard_name+'.end', $scope.current)
            
            $rootScope.$on($scope.wizard_name+'.afterChange',(ev, {event, slick, currentSlide, nextSlide})=>{
                $scope.current = currentSlide;
                $scope.is_end = currentSlide === $scope.items.length-1
            })
            $rootScope.$on($scope.wizard_name+'.init',(event, slick, currentSlide, nextSlide)=>{
            })
    
        }]
    }
}
