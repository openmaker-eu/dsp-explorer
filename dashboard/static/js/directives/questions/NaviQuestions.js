export default function(){
    return {
        template:`
            <span ng-class="{'transparent':is_start}" class="pointer " ng-click="prev()">
                <h1><i class="fas fa-chevron-left text-brown"></i></h1>
                <h4>&nbsp;PREVIOUS</h4>
            </span>
            <span style="text-align:center;">
                <i
                    ng-repeat="(q_index, items) in [].constructor(items.length) track by $index"
                    class="fa-circle text-brown margin-10-perc"
                    ng-class="{'fas': q_index == current, 'far' :q_index !== current}"
                ></i>
            </span>
            <span ng-if="!is_end" class="pointer" ng-click="next()">
                <h4>NEXT&nbsp;</h4>
                <h1><i class="fas fa-chevron-right text-brown"></i></h1>
            </span>
            <span ng-if="is_end" ng-click="end()" class="pointer sup-next">
                <h4>CLOSE&nbsp;&nbsp;</h4>
                <h1><i class="far fa-times-circle text-brown"></i></h1>
            </span>
        `,
        scope: {
            items:'=',
            wizardid:'='
        },
        controller : ['$scope','$rootScope', function($scope, $rootScope){
            
            $scope.wizard_name = 'wizard.'+$scope.wizardid
            $scope.is_start = true
            $scope.is_end = false
            $scope.current = 0;
            
            $scope.prev=()=>$rootScope.$emit($scope.wizard_name+'.prev', $scope.current)
            $scope.next=()=>$rootScope.$emit($scope.wizard_name+'.next', $scope.current)
            $scope.end=()=>$rootScope.$emit($scope.wizard_name+'.end', $scope.current)
            
            $rootScope.$on($scope.wizard_name+'.afterChange',(ev, {event, slick, currentSlide, nextSlide})=>{
                $scope.current = currentSlide;
                $scope.is_start = currentSlide === 0
                $scope.is_end = currentSlide === $scope.items.length-1
                //$('.slick-current').find('input, select').first().focus().select().click()
            })
            $rootScope.$on($scope.wizard_name+'.init',(event, slick, currentSlide, nextSlide)=>{
                //@TODO: substutite with event
                //slick.slickGoTo($scope.current);
            })
            
            window.onkeypress = (e)=> { e.which=== 13 && $scope.next()}
    
        }]
    }
}
