import * as _ from 'lodash'

let template = `
   
    <div class="modal-body padding-5-perc">
    
        <entity-loading
                ng-if="!questions"
                class="text-center"
                loading="questions.length == 0"
                entityname=""
                custommessage="Loading your questions"
        ></entity-loading>
        
        <entity-loading
                ng-if="loading"
                class="text-center"
                loading="loading"
                entityname=""
                custommessage="Saving data"
        ></entity-loading>
    
        <div ng-show="!loading">
        
            <form name="wizard.form" ng-if="questions">
                <slick class="col-md-12 modal-slider" settings="slickConfig" prev-arrow=".sup-prev" next-arrow=".sup-next">
                    <question ng-repeat="question in questions" data="question" model="wizard.formmodel" ></question>
                </slick>
            </form>
           
            <div class="col-md-12 step-navigation">
                
                <span ng-class="{'transparent':is_start}" class="pointer " ng-click="prev()">
                    <h1><i class="glyphicon glyphicon-menu-left text-brown"></i></h1>
                    <h4>&nbsp;PREVIOUS</h4>
                </span>
               
                <span style="text-align:center;">
                    <i
                        ng-repeat="(q_index, question) in [].constructor(questions.length) track by $index"
                        class="fa text-brown margin-10-perc"
                        ng-class="{'fa-circle-o': q_index == current, 'fa-circle' :q_index !== current}"
                    ></i>
                </span>
                
                <span ng-if="!is_end" class="pointer" ng-click="next()">
                    <h4>NEXT&nbsp;</h4>
                    <h1><i class="glyphicon glyphicon-menu-right text-brown"></i></h1>
                </span>
                
                <span ng-if="is_end" ng-click="close()" class="pointer sup-next">
                    <h4>CLOSE&nbsp;&nbsp;</h4>
                    <h1><i class="fa fa-times-circle-o text-brown"></i></h1>
                </span>
                
            </div>
        </div>

    </div>
`

export default ['$rootScope', '$uibModal', function($rootScope, $uibModal){
    
    let F = {
        open: n=>{
            F.modalInstance = $uibModal.open({
                template: template,
                backdrop: true,
                windowClass: 'signup-modal',
                transclude:true,
                controller: ['$scope', '$http', function($scope, $http){
    
                    $scope.current = 0;
                    $scope.is_start = true
                    $scope.is_end = false
                    $scope.slick = null
                    $scope.wizard = {form:{}, formmodel:{}}
                    
                    $scope.questions = null
                    $scope.loading = false
                    $scope.error = false
                    
                    $scope.close = ()=>{ F.modalInstance.close() }

                    $http.get('/api/v1.4/questions/').then((res)=>{$scope.questions = res.data.questions})
                    
                    $scope.submit = (url=false)=>{
                        let call = $http.put(_.isString(url) ? url : '/api/v1.4/questions/', $scope.wizard.formmodel)
                        return call
                    }
                    
                    $scope.next = ()=>{
    
                        let question = _.get($scope , 'questions['+$scope.current+']')
                        let form = $scope.wizard.form
                        let subform = $scope.wizard.form[question.name]
 
                        // Stop if invalid data on current step
                        if(subform && subform.hasOwnProperty('$invalid') && subform.$invalid) {
                            subform.$$element.find('.submit').click()
                            return
                        }
    
                        // Perform apicall
                        if( question && question.apicall ){
                            $scope.loading=true;
                            $scope.submit(question.apicall).then(()=>{
                                    $scope.loading=false;
                                    $scope.slickConfig.method.slickNext()
                                },
                                (res)=>{$scope.loading=false; question.error=res.data.error; console.log(res);})
                        }
                        else
                            $scope.slickConfig.method.slickNext()

                        
                    }
                    $scope.prev = ()=>{
                        $scope.slickConfig.method.slickPrev()
                    }
    
                    $scope.slickConfig ={
                        method:{},
                        event: {},
                        events: {},
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
                                $scope.is_end = currentSlide+1 === $scope.questions.length
                                // $('.slick-current').find('input, select').focus().select().click()
                                
                            },
                            beforeChange: (event, slick, currentSlide, nextSlide)=>{
                                
                                console.log(currentSlide, nextSlide, event, slick);
                               
                                
                            },
                            init: function (event, slick) {
                                slick.slickGoTo($scope.current);
                                window.onkeypress = (e)=> {e.which=== 13&& $scope.next()}
                            }
                        }
                    }
                    
                }]
            });
        }
    }
    
    
    
    $rootScope.$on('question.modal.open', F.open)
    return F
    
}]