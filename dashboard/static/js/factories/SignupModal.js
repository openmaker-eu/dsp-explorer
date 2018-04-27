import * as _ from 'lodash'

let template = `
    
    <div class="modal-body padding-5-perc" ng-if="!steps">
             <entity-loading
                class="text-center"
                loading="steps.lenght == 0"
                entityname=""
                custommessage="Loading your questions"
             ></entity-loading>
    </div>
    <ng-form class="modal-body padding-5-perc" ng-if="steps">
    
        <slick
            class="col-md-12 modal-slider"
            settings="slickConfig"
            prev-arrow=".sup-prev"
            next-arrow=".sup-next"
        >
            <signup-template ng-repeat="step in steps" type="{$ step.type $}" data="step.data" label="{$ step.label $}"></signup-template>
            <signup-template  type="close" label="Thank you!"></signup-template>
        </slick>

        <div class="col-md-12 step-navigation">
            
            <span ng-class="{'transparent':is_start}" class="pointer sup-prev ">
                <h1><i class="glyphicon glyphicon-menu-left text-brown"></i></h1>
                <h4>&nbsp;PREVIOUS</h4>
            </span>
            
            <span style="text-align:center;">
                <i
                    ng-repeat="(step_index, step) in [].constructor(steps.length) track by $index"
                    class="fa text-brown margin-10-perc"
                    ng-class="{'fa-circle-o': step_index == current, 'fa-circle' :step_index !== current}"
                ></i>
            </span>
            
            <span ng-if="!is_end" class="pointer sup-next">
                <h4>NEXT&nbsp;</h4>
                <h1><i class="glyphicon glyphicon-menu-right text-brown"></i></h1>
            </span>
            
            <span ng-if="is_end" ng-click="close()" class="pointer sup-next">
                <h4>CLOSE&nbsp;&nbsp;</h4>
                <h1><i class="fa fa-times-circle-o text-brown"></i></h1>
            </span>
            
        </div>

    </ng-form>
`

export default ['$http', '$rootScope', '$uibModal', '$sce', '$timeout',  function($http, $rootScope, $uibModal, $sce, $timeout){
    
    let factory = {
        open: n=>{
            factory.modalInstance = $uibModal.open({
                template: template,
                backdrop: true,
                windowClass: 'signup-modal',
                controller: [ '$scope', function($scope){
    
                    $scope.current = 0;
                    $scope.is_start = true
                    $scope.is_end = false
                    
                    $scope.steps = null
                    $scope.close = ()=>{ factory.modalInstance.close() }

                    $http.get('/api/v1.4/questions/').then((res)=>{
                        $scope.steps = res.data.questions
                    })
  
                    
                    $scope.slickConfig ={
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        draggable: false,
                        autoplay: false,
                        arrows: true,
                        infinite: false,
                        event: {
                            afterChange: function (event, slick, currentSlide, nextSlide) {
                                $scope.current = currentSlide;
                                $scope.is_start = currentSlide === 0
                                $scope.is_end = currentSlide === $scope.steps.length
                                
                                $('.slick-current').find('input, select').focus().select().click()
                                
                            },
                            edge: function(event, slick, direction){ console.log(direction); },
                            init: function (event, slick) {
                                slick.slickGoTo($scope.current);
                                window.onkeypress = (e)=> {e.which=== 13&& slick.slickNext()}
                            }
                        }
                    }
                    
            
                }]
            });
        }
    }
    
    $rootScope.$on('signup.modal.open', factory.open)
    return factory
    
}]