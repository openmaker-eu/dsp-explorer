export default function(){
    return {
        template:`
            <div class="col-md-12 step-navigation" ng-show="items">
                <div ng-if="action='chatbot.question.simple'" style="display: flex; flex-direction:row; justify-content: center; padding-bottom:3%;">
                    <div ng-repeat="act in items[current].actions.options" style="padding:1%;">
                        <button class="btn btn-danger pull-left capitalize" ng-click="next(act.value || act.label || act)">{$ act.label || act.value || act $}</button>
                    </div>
                </div>
            </div>
            
        `,
        scope: {
            items:'=',
            wizardid:'='
        },
        controller : ['$scope','$rootScope', function($scope, $rootScope){
            
            console.log('NAVI CHAT', $scope.wizardid);
            
            $scope.wizard_name = 'wizard.'+$scope.wizardid
            $scope.is_end = false
            $scope.current = 0;
            
            $scope.prev=()=>$rootScope.$emit($scope.wizard_name+'.prev', $scope.current)
            $scope.next=(value)=> {
                if(value === 'goto:last') $scope.goto($scope.items.length-1)
                
                $scope.items[$scope.current].feedback = value
                $rootScope.$emit($scope.wizard_name+'.next', $scope.current)
                $scope.is_end && $scope.end()
            }
            
            $scope.end=()=>$rootScope.$emit($scope.wizard_name+'.end', $scope.current)
            $scope.goto=(question_index)=>$rootScope.$emit($scope.wizard_name+'.goto', question_index)
            
            $rootScope.$on($scope.wizard_name+'.afterChange',(ev, {event, slick, currentSlide, nextSlide})=>{
                $scope.current = currentSlide;
                $scope.is_end = currentSlide === $scope.items.length-1
            })
    
        }]
    }
}
