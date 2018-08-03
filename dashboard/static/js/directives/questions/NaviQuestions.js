export default function(){
    return {
        template:`
            <div class="col-md-12 wizard-navi" ng-show="items">

                <!--Standard prev button-->
                <span ng-class="{'transparent':is_start}" ng-if="!is_custom_prev" class="pointer " ng-click="prev()">
                    <h1><i class="fas fa-chevron-left text-brown"></i></h1>
                    <h4>&nbsp;PREVIOUS</h4>
                </span>
                 <!--Custom prev button-->
                <span class="pointer" ng-if="is_custom_prev" ng-bind-html="custom_prev" ng-click="prev()"></span>
                
                <span ng-show="!nodots" class="no-mobile" style="text-align:center;">
                    <i
                        ng-repeat="(q_index, items) in [].constructor(items.length) track by $index"
                        class="fa-circle text-brown margin-10-perc"
                        ng-class="{'fas': q_index == current, 'far' :q_index !== current}"
                    ></i>
                </span>
                
                <!--Standard next button-->
                <span ng-if="!is_end && !is_custom_next" class="pointer" ng-click="next()">
                    <h4>NEXT&nbsp;</h4>
                    <h1><i class="fas fa-chevron-right text-brown"></i></h1>
                </span>
                <!--End button-->
                <span ng-if="is_end && !is_custom_next" ng-click="end()" class="pointer sup-next">
                    <h4>CLOSE&nbsp;&nbsp;</h4>
                    <h1><i class="far fa-times-circle text-brown"></i></h1>
                </span>
                <!--Custom next button-->
                <span ng-if="is_custom_next" ng-click="is_end? end(): next()" ng-bind-html="custom_next" class="pointer sup-next"></span>
                
            </div>
        `,
        scope: {
            items:'=',
            wizardid:'=',
            nodots:'='
        },
        controller : ['$scope','$rootScope', function($scope, $rootScope){
            $scope.wizard_name = 'wizard.'+$scope.wizardid
            $scope.is_start = true
            $scope.is_end = false
            $scope.current = 0;
            
            $scope.prev=()=>$rootScope.$emit($scope.wizard_name+'.prev', $scope.current)
            $scope.next=()=>$rootScope.$emit($scope.wizard_name+'.next', $scope.current)
            $scope.end=()=>$rootScope.$emit($scope.wizard_name+'.end', $scope.current)
            
            let custom_buttons = ()=>{
                let question = $scope.items && $scope.items[$scope.current]
    
                $scope.is_custom_next = $scope.items[$scope.current].hasOwnProperty('custom_next')
                $scope.is_custom_prev = $scope.items[$scope.current].hasOwnProperty('custom_prev')
                
                $scope.custom_next = $scope.items[$scope.current]['custom_next']
                $scope.custom_prev = $scope.items[$scope.current]['custom_prev']
                
            }
            
            $rootScope.$on($scope.wizard_name+'.afterChange',(ev, {event, slick, currentSlide, nextSlide})=>{
                $scope.current = currentSlide
                $scope.is_start = currentSlide === 0
                $scope.is_end = currentSlide === $scope.items.length-1
                $scope.custom_button = $scope.items && $scope.items[$scope.current]
                //$('.slick-current').find('input, select').first().focus().select().click()
                custom_buttons()
            })
            $rootScope.$on($scope.wizard_name+'.init',(event, slick, currentSlide, nextSlide)=>{
                custom_buttons()
            })

        }]
    }
}
