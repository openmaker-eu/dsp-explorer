export default function(){
    return {
        template:`
            <div class="col-md-12 step-navigation" ng-show="items">
                <div
                    ng-if="action='chatbot.question.simple'"
                    style="display: flex; flex-direction: row; justify-content: center; align-items: center; padding-bottom:5%;"
                >
                    
                    <div
                        ng-if="!items[current].actions.type || items[current].actions.type == 'buttons'"
                        ng-repeat="act in items[current].actions.options"
                        style="padding:1%;"
                    >
                        <button
                            class="btn btn-danger pull-left capitalize"
                            ng-click="next(act.value || act.label || act)"
                        >{$ act.label || act.value || act $}</button>
                    </div>
                    
                    <div ng-if="items[current].actions.type == 'stars'" ng-init="rating={value:-1}">
                        <span
                            ng-repeat="a in get_stars(items[current].actions.amount) track by $index"
                            ng-click="next($index+1)"
                            ng-mouseover="rating.value=$index"
                            ng-mouseleave="rating.value=-1"
                            ng-class="{'fas': $index<=rating.value, 'far':$index>rating.value}"
                            class="fa-star fa-2x text-red pointer"
                        ></span>
                    </div>
                </div>
            </div>
            
        `,
        scope: {
            items:'=',
            wizardid:'='
        },
        controller : ['$scope','$rootScope', function($scope, $rootScope){
            
            $scope.wizard_name = 'wizard.'+$scope.wizardid
            $scope.is_end = $scope.items && $scope.items.length < 2
            $scope.current = 0;
            
            $scope.prev=()=>$rootScope.$emit($scope.wizard_name+'.prev', $scope.current)
            $scope.next=(value)=> {
                
                if(value === 'goto:last') $scope.goto($scope.items.length-1)
                if(value.includes('event:')) $rootScope.$emit(value.split(':')[1])
                
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
            
            $scope.get_stars = (amount)=>[...new Array(amount)]
    
            $rootScope.$on('chatbot.close',()=>$scope.end())
    
        }]
    }
}
